import { Injectable } from '@angular/core';
import imageCompression from 'browser-image-compression';

export interface ImageValidationResult {
  valid: boolean;
  error?: string;
}

export interface ImageValidationOptions {
  maxFiles: number;
  currentFileCount: number;
  maxSizeBytes?: number;
}

@Injectable({
  providedIn: 'root'
})
export class ImageProcessingService {
  private readonly MAX_SIZE_MB = 5;
  private readonly MAX_DIMENSION = 2048;

  /**
   * Validate a single file
   */
  validateFile(file: File, options: ImageValidationOptions): ImageValidationResult {
    // Check if it's an image
    if (!file.type.startsWith('image/')) {
      return {
        valid: false,
        error: `${file.name}: Not an image file`
      };
    }

    // Check max files limit
    if (options.currentFileCount >= options.maxFiles) {
      return {
        valid: false,
        error: `Maximum ${options.maxFiles} images allowed`
      };
    }

    return { valid: true };
  }

  /**
   * Validate multiple files
   */
  validateFiles(files: File[], options: ImageValidationOptions): {
    validFiles: File[];
    errors: string[];
  } {
    const validFiles: File[] = [];
    const errors: string[] = [];
    let currentCount = options.currentFileCount;

    for (const file of files) {
      const result = this.validateFile(file, {
        ...options,
        currentFileCount: currentCount
      });

      if (result.valid) {
        validFiles.push(file);
        currentCount++;
      } else if (result.error) {
        errors.push(result.error);
      }
    }

    return { validFiles, errors };
  }

  /**
   * Check for duplicate files by name
   */
  filterDuplicates(files: File[], existingFileNames: Set<string>): {
    uniqueFiles: File[];
    hasDuplicates: boolean;
  } {
    const uniqueFiles = files.filter(f => !existingFileNames.has(f.name));
    const hasDuplicates = uniqueFiles.length < files.length;

    return { uniqueFiles, hasDuplicates };
  }

  /**
   * Compress an image using browser-image-compression library
   */
  async compressImage(file: File): Promise<File> {
    const maxSizeBytes = this.MAX_SIZE_MB * 1024 * 1024;

    // If file is already small enough, return it
    if (file.size <= maxSizeBytes) {
      return file;
    }

    try {
      const options = {
        maxSizeMB: this.MAX_SIZE_MB,
        maxWidthOrHeight: this.MAX_DIMENSION,
        useWebWorker: true,
        fileType: 'image/jpeg' as const,
        initialQuality: 0.9
      };

      const compressedFile = await imageCompression(file, options);

      // Return compressed file with original filename
      return new File([compressedFile], file.name, {
        type: 'image/jpeg',
        lastModified: Date.now()
      });
    } catch (error) {
      console.error('Error compressing image:', error);
      throw new Error(`Failed to compress ${file.name}`);
    }
  }

  /**
   * Create a preview URL for an image file
   */
  async createPreviewUrl(file: File): Promise<string> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        const result = e.target?.result;
        if (typeof result === 'string') {
          resolve(result);
        } else {
          reject(new Error('Failed to create preview URL'));
        }
      };
      reader.onerror = () => reject(new Error('Failed to read file'));
      reader.readAsDataURL(file);
    });
  }

  /**
   * Revoke a preview URL to free memory
   */
  revokePreviewUrl(url: string): void {
    if (url.startsWith('blob:')) {
      URL.revokeObjectURL(url);
    }
  }

  /**
   * Process a file: compress and create preview
   */
  async processImageFile(file: File): Promise<{ compressedFile: File; previewUrl: string }> {
    const compressedFile = await this.compressImage(file);
    const previewUrl = await this.createPreviewUrl(compressedFile);

    return { compressedFile, previewUrl };
  }
}

