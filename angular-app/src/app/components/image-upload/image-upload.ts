import { Component, output, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';

export interface ImageFile {
  file: File;
  previewUrl: string;
}

@Component({
  selector: 'app-image-upload',
  imports: [FormsModule],
  templateUrl: './image-upload.html',
  styleUrl: './image-upload.scss'
})
export class ImageUpload {
  readonly imageFiles = signal<ImageFile[]>([]);
  readonly filesChanged = output<File[]>();
  readonly newImageUrl = signal<string>('');
  readonly error = signal<string | null>(null);

  onFileSelect(event: Event) {
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

    // Convert files to data URLs for preview and store File objects
    files.forEach(file => {
      const reader = new FileReader();
      reader.onload = (e) => {
        const previewUrl = e.target?.result as string;
        this.addImageFile(file, previewUrl);
      };
      reader.readAsDataURL(file);
    });

    // Reset input
    input.value = '';
  }

  addImageUrlFromInput() {
    const url = this.newImageUrl().trim();
    if (!url) return;

    // Basic URL validation
    try {
      new URL(url);
      // Create a fake file object for URL-based images (not recommended but supported)
      this.error.set('Please upload files directly instead of using URLs for better quality');
      this.newImageUrl.set('');
    } catch {
      this.error.set('Please enter a valid URL');
    }
  }

  private addImageFile(file: File, previewUrl: string) {
    const current = this.imageFiles();
    if (current.length >= 10) {
      this.error.set('Maximum 10 images allowed');
      return;
    }
    const newFiles = [...current, { file, previewUrl }];
    this.imageFiles.set(newFiles);
    this.filesChanged.emit(newFiles.map(f => f.file));
  }

  removeImage(index: number) {
    const current = this.imageFiles();
    const newFiles = current.filter((_, i) => i !== index);
    this.imageFiles.set(newFiles);
    this.filesChanged.emit(newFiles.map(f => f.file));
    this.error.set(null);
  }

  clearError() {
    this.error.set(null);
  }
}
