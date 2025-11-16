import { Component, output, signal, inject } from '@angular/core';
import { UploadsService } from '../../services/uploads.service';

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
export class ImageUpload {
  private uploadsService = inject(UploadsService);

  readonly imageFiles = signal<ImageFile[]>([]);
  readonly imageIdsChanged = output<string[]>();
  readonly error = signal<string | null>(null);

  async onFileSelect(event: Event) {
    const input = event.target as HTMLInputElement;
    if (!input.files) return;

    const files = Array.from(input.files);

    // Validate file types and sizes
    for (const file of files) {
      if (!file.type.startsWith('image/')) {
        this.error.set('Please select only image files');
        return;
      }
      if (file.size > 5 * 1024 * 1024) { // 5MB limit
        this.error.set('Images must be smaller than 5MB');
        return;
      }
    }

    const currentFiles = this.imageFiles();
    if (currentFiles.length + files.length > 10) {
      this.error.set('Maximum 10 images allowed');
      return;
    }

    this.error.set(null);

    // Convert files to data URLs for preview and upload to backend
    for (const file of files) {
      const reader = new FileReader();
      reader.onload = async (e) => {
        const previewUrl = e.target?.result as string;
        await this.addImageFileAndUpload(file, previewUrl);
      };
      reader.readAsDataURL(file);
    }

    // Reset input
    input.value = '';
  }

  private async addImageFileAndUpload(file: File, previewUrl: string) {
    const current = this.imageFiles();
    if (current.length >= 10) {
      this.error.set('Maximum 10 images allowed');
      return;
    }

    // Add image with temporary ID and uploading state
    const tempImageFile: ImageFile = {
      id: '',
      file,
      previewUrl,
      isUploading: true
    };

    const newFiles = [...current, tempImageFile];
    this.imageFiles.set(newFiles);

    // Upload to backend
    try {
      const uploadResult = await this.uploadsService.uploadImage(file).toPromise();

      // Update with real ID from backend
      const updatedFiles = this.imageFiles().map(img =>
        img.file === file
          ? { ...img, id: uploadResult!.id, isUploading: false }
          : img
      );
      this.imageFiles.set(updatedFiles);

      // Emit updated IDs
      this.emitImageIds();
    } catch (error) {
      console.error('Error uploading image:', error);

      // Mark upload as failed
      const updatedFiles = this.imageFiles().map(img =>
        img.file === file
          ? { ...img, isUploading: false, uploadError: 'Upload failed' }
          : img
      );
      this.imageFiles.set(updatedFiles);
    }
  }

  async removeImage(index: number) {
    const current = this.imageFiles();
    const imageToRemove = current[index];

    // If image was uploaded, delete from backend
    if (imageToRemove.id) {
      try {
        // await this.uploadsService.deleteImage(imageToRemove.id).toPromise();
      } catch (error) {
        console.error('Error deleting image from backend:', error);
      }
    }

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
}
