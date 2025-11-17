import { Component, output, signal, inject, OnDestroy } from '@angular/core';
import { ImageProcessingService } from '../../services/image-processing.service';
import { UploadsService } from '../../services/uploads.service';
import { Subscription } from 'rxjs';

export interface ImageFile {
  id: string;
  file: File;
  previewUrl: string;
  isUploading: boolean;
  uploadError?: string;
}

@Component({
  selector: 'app-image-upload',
  imports: [],
  templateUrl: './image-upload.html',
  styleUrl: './image-upload.scss'
})
export class ImageUpload implements OnDestroy {
  private imageProcessingService = inject(ImageProcessingService);
  private uploadsService = inject(UploadsService);

  private uploadSubscriptions = new Map<File, Subscription>();
  private readonly MAX_FILES = 10;

  readonly imageFiles = signal<ImageFile[]>([]);
  readonly imageIdsChanged = output<string[]>();
  readonly error = signal<string | null>(null);
  readonly isUploading = signal<boolean>(false);

  async onFileSelect(event: Event) {
    const input = event.target as HTMLInputElement;
    if (!input.files) return;

    const files = Array.from(input.files);

    // Validate files
    const { validFiles, errors } = this.imageProcessingService.validateFiles(files, {
      maxFiles: this.MAX_FILES,
      currentFileCount: this.imageFiles().length
    });

    // Check for duplicates
    const currentFiles = this.imageFiles();
    const existingFileNames = new Set(currentFiles.map(f => f.file.name));
    const { uniqueFiles, hasDuplicates } = this.imageProcessingService.filterDuplicates(
      validFiles,
      existingFileNames
    );

    // Set error messages
    if (errors.length > 0) {
      this.error.set(errors.join('; '));
    } else if (hasDuplicates) {
      this.error.set('Some files were already added and were skipped');
    } else {
      this.error.set(null);
    }

    if (uniqueFiles.length === 0) {
      input.value = '';
      return;
    }


    this.isUploading.set(true);

    for (const file of uniqueFiles) {
      await this.processFile(file);
    }

    this.isUploading.set(false);
    input.value = '';
  }

  private async processFile(file: File): Promise<void> {
    try {
      // Use ImageProcessingService to compress and create preview
      const { compressedFile, previewUrl } = await this.imageProcessingService.processImageFile(file);
      await this.addImageFileAndUpload(compressedFile, previewUrl);
    } catch (error) {
      console.error('Error processing file:', error);
      this.error.set(`Failed to process ${file.name}`);
    }
  }


  private async addImageFileAndUpload(file: File, previewUrl: string) {
    const current = this.imageFiles();
    if (current.length >= this.MAX_FILES) {
      this.error.set(`Maximum ${this.MAX_FILES} images allowed`);
      return;
    }

    const tempImageFile: ImageFile = {
      id: '',
      file,
      previewUrl,
      isUploading: true
    };

    const newFiles = [...current, tempImageFile];
    this.imageFiles.set(newFiles);

    // Upload directly using UploadsService
    const subscription = this.uploadsService.uploadImage(file).subscribe({
      next: (uploadResult) => {
        // Update with real ID from backend
        const updatedFiles = this.imageFiles().map(img =>
          img.file === file
            ? { ...img, id: uploadResult.id, isUploading: false }
            : img
        );
        this.imageFiles.set(updatedFiles);
        this.emitImageIds();
        this.uploadSubscriptions.delete(file);
      },
      error: (error) => {
        console.error('Error uploading image:', error);
        // Mark upload as failed
        const updatedFiles = this.imageFiles().map(img =>
          img.file === file
            ? { ...img, isUploading: false, uploadError: 'Upload failed' }
            : img
        );
        this.imageFiles.set(updatedFiles);
        this.uploadSubscriptions.delete(file);
      }
    });

    this.uploadSubscriptions.set(file, subscription);
  }

  removeImage(index: number) {
    const current = this.imageFiles();
    const imageToRemove = current[index];

    // Cancel pending upload if any
    const subscription = this.uploadSubscriptions.get(imageToRemove.file);
    if (subscription) {
      subscription.unsubscribe();
      this.uploadSubscriptions.delete(imageToRemove.file);
    }

    // Revoke preview URL to prevent memory leak
    this.imageProcessingService.revokePreviewUrl(imageToRemove.previewUrl);

    // Remove from local array
    const newFiles = current.filter((_, i) => i !== index);
    this.imageFiles.set(newFiles);
    this.emitImageIds();
  }

  private emitImageIds() {
    const ids = this.imageFiles()
      .filter(img => img.id && !img.uploadError)
      .map(img => img.id);
    this.imageIdsChanged.emit(ids);
  }

  clearError() {
    this.error.set(null);
  }

  ngOnDestroy() {
    // Cancel all pending uploads
    this.uploadSubscriptions.forEach(sub => sub.unsubscribe());
    this.uploadSubscriptions.clear();

    // Revoke all preview URLs to prevent memory leaks
    this.imageFiles().forEach(img => {
      this.imageProcessingService.revokePreviewUrl(img.previewUrl);
    });
  }
}
