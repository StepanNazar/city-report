import { Component, input, output, signal, inject, OnDestroy, effect } from '@angular/core';
import { ImageProcessingService } from '../../services/image-processing.service';
import { UploadsService } from '../../services/uploads.service';
import { ImageResponse } from '../../services/posts.service';
import { Subscription } from 'rxjs';

export interface EditableImage {
    id: string;
    url: string;
    isExisting: boolean;
    file?: File;
    previewUrl?: string;
    isUploading?: boolean;
    uploadError?: string;
}

@Component({
    selector: 'app-image-edit',
    imports: [],
    templateUrl: './image-edit.html',
    styleUrl: './image-edit.scss'
})
export class ImageEdit implements OnDestroy {
    private imageProcessingService = inject(ImageProcessingService);
    private uploadsService = inject(UploadsService);

    private uploadSubscriptions = new Map<File, Subscription>();
    private readonly MAX_FILES = 10;
    private readonly uniqueId = `image-edit-${Math.random().toString(36).substring(2, 9)}`;

    readonly existingImages = input<ImageResponse[]>([]);
    readonly imageIdsChanged = output<string[]>();

    readonly images = signal<EditableImage[]>([]);
    readonly error = signal<string | null>(null);
    readonly isUploading = signal<boolean>(false);

    get inputId(): string {
        return this.uniqueId;
    }

    constructor() {
        // Initialize images from existing images
        effect(() => {
            const existing = this.existingImages();
            // Only initialize once when component is created
            if (this.images().length === 0 && existing && existing.length > 0) {
                const editableImages: EditableImage[] = existing.map(img => ({
                    id: img.id,
                    url: img.url,
                    isExisting: true
                }));
                this.images.set(editableImages);
                this.emitImageIds();
            }
        });
    }

    async onFileSelect(event: Event) {
        console.log('[ImageEdit] onFileSelect triggered', event);
        const input = event.target as HTMLInputElement;
        if (!input.files) {
            console.log('[ImageEdit] No files selected');
            return;
        }

        const files = Array.from(input.files);
        console.log('[ImageEdit] Files selected:', files.length, files);
        const currentCount = this.images().length;
        console.log('[ImageEdit] Current images count:', currentCount);

        // Validate files
        const { validFiles, errors } = this.imageProcessingService.validateFiles(files, {
            maxFiles: this.MAX_FILES,
            currentFileCount: currentCount
        });
        console.log('[ImageEdit] Validation result:', { validFiles: validFiles.length, errors });

        // Check for duplicates
        const currentFiles = this.images().filter(img => img.file).map(img => img.file!.name);
        const existingFileNames = new Set(currentFiles);
        const { uniqueFiles, hasDuplicates } = this.imageProcessingService.filterDuplicates(
            validFiles,
            existingFileNames
        );
        console.log('[ImageEdit] Duplicate check:', { uniqueFiles: uniqueFiles.length, hasDuplicates });

        // Set error messages
        if (errors.length > 0) {
            this.error.set(errors.join('; '));
        } else if (hasDuplicates) {
            this.error.set('Some files were already added and were skipped');
        } else {
            this.error.set(null);
        }

        if (uniqueFiles.length === 0) {
            console.log('[ImageEdit] No unique files to process');
            input.value = '';
            return;
        }

        this.isUploading.set(true);
        console.log('[ImageEdit] Starting upload process');

        for (const file of uniqueFiles) {
            await this.processFile(file);
        }

        this.isUploading.set(false);
        console.log('[ImageEdit] Upload process completed');
        input.value = '';
    }

    private async processFile(file: File): Promise<void> {
        console.log('[ImageEdit] Processing file:', file.name);
        try {
            const { compressedFile, previewUrl } = await this.imageProcessingService.processImageFile(file);
            console.log('[ImageEdit] File processed successfully:', { compressedFile: compressedFile.name, previewUrl });
            await this.addImageFileAndUpload(compressedFile, previewUrl);
        } catch (error) {
            console.error('[ImageEdit] Error processing file:', error);
            this.error.set(`Failed to process ${file.name}`);
        }
    }

    private async addImageFileAndUpload(file: File, previewUrl: string) {
        console.log('[ImageEdit] Adding image and uploading:', file.name);
        const current = this.images();
        console.log('[ImageEdit] Current images before add:', current.length);

        if (current.length >= this.MAX_FILES) {
            console.log('[ImageEdit] Max files reached');
            this.error.set(`Maximum ${this.MAX_FILES} images allowed`);
            return;
        }

        const tempImage: EditableImage = {
            id: '',
            url: previewUrl,
            isExisting: false,
            file,
            previewUrl,
            isUploading: true
        };

        const newImages = [...current, tempImage];
        console.log('[ImageEdit] Setting new images array, length:', newImages.length);
        this.images.set(newImages);

        // Upload directly using UploadsService
        console.log('[ImageEdit] Starting upload to server');
        const subscription = this.uploadsService.uploadImage(file).subscribe({
            next: (uploadResult) => {
                console.log('[ImageEdit] Upload successful:', uploadResult);
                // Update with real ID from backend
                const updatedImages = this.images().map(img =>
                    img.file === file
                        ? { ...img, id: uploadResult.id, url: uploadResult.url, isUploading: false }
                        : img
                );
                this.images.set(updatedImages);
                this.emitImageIds();
                this.uploadSubscriptions.delete(file);
            },
            error: (error) => {
                console.error('[ImageEdit] Error uploading image:', error);
                const updatedImages = this.images().map(img =>
                    img.file === file
                        ? { ...img, isUploading: false, uploadError: 'Upload failed' }
                        : img
                );
                this.images.set(updatedImages);
                this.uploadSubscriptions.delete(file);
            }
        });

        this.uploadSubscriptions.set(file, subscription);
    }

    removeImage(index: number) {
        const current = this.images();
        const imageToRemove = current[index];

        // Cancel pending upload if any
        if (imageToRemove.file) {
            const subscription = this.uploadSubscriptions.get(imageToRemove.file);
            if (subscription) {
                subscription.unsubscribe();
                this.uploadSubscriptions.delete(imageToRemove.file);
            }
        }

        // Revoke preview URL to prevent memory leak (only for new uploads)
        if (imageToRemove.previewUrl && !imageToRemove.isExisting) {
            this.imageProcessingService.revokePreviewUrl(imageToRemove.previewUrl);
        }

        // Remove from array
        const newImages = current.filter((_, i) => i !== index);
        this.images.set(newImages);
        this.emitImageIds();
    }

    moveImageUp(index: number) {
        if (index === 0) return;

        const current = [...this.images()];
        [current[index - 1], current[index]] = [current[index], current[index - 1]];
        this.images.set(current);
        this.emitImageIds();
    }

    moveImageDown(index: number) {
        const current = [...this.images()];
        if (index === current.length - 1) return;

        [current[index], current[index + 1]] = [current[index + 1], current[index]];
        this.images.set(current);
        this.emitImageIds();
    }

    private emitImageIds() {
        const ids = this.images()
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

        // Revoke preview URLs for new uploads only
        this.images().forEach(img => {
            if (img.previewUrl && !img.isExisting) {
                this.imageProcessingService.revokePreviewUrl(img.previewUrl);
            }
        });
    }
}

