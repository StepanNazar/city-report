import { Component, inject, OnInit, signal, ViewChild, ChangeDetectionStrategy } from '@angular/core';
import { Router } from '@angular/router';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { LocationSelector } from '../../components/location-selector/location-selector.component';
import { Map, Coordinates } from '../../components/map/map';
import { ImageUpload } from '../../components/image-upload/image-upload';
import { AuthenticationService } from '../../services/authentication-service';
import { PostsService } from '../../services/posts.service';
import { UploadsService } from '../../services/uploads.service';
import { NotificationService } from '../../services/notification.service';
import { LocationOption, LocationSelectorService, ReverseGeocodingResult } from '../../services/location-selector-service';

@Component({
  selector: 'app-create-post-page',
  imports: [LocationSelector, Map, ImageUpload, ReactiveFormsModule],
  templateUrl: './create-post-page.html',
  styleUrl: './create-post-page.scss',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class CreatePostPage implements OnInit {
  private authService = inject(AuthenticationService);
  private postsService = inject(PostsService);
  private uploadsService = inject(UploadsService);
  private notificationService = inject(NotificationService);
  private router = inject(Router);
  private locationSelectorService = inject(LocationSelectorService);

  @ViewChild(ImageUpload) imageUploadComponent?: ImageUpload;

  readonly isSubmitting = signal<boolean>(false);
  readonly selectedLocation = signal<LocationOption | null>(null);
  readonly selectedCoordinates = signal<Coordinates | null>(null);
  readonly imageFiles = signal<File[]>([]);
  readonly reverseGeocodedLocation = signal<ReverseGeocodingResult | null>(null);

  postForm = new FormGroup({
    title: new FormControl('', [
      Validators.required,
      Validators.minLength(1),
      Validators.maxLength(100)
    ]),
    body: new FormControl('', [
      Validators.required,
      Validators.minLength(1),
      Validators.maxLength(10000)
    ])
  });

  ngOnInit() {
    // Check if user is logged in
    const token = this.authService.getAccessToken();
    if (!token) {
      this.notificationService.error('You must be logged in to create a post', 5000);
      this.router.navigate(['/signin']);
    }
  }

  onLocationSelected(location: LocationOption | null) {
    this.selectedLocation.set(location);
    if (location) {
      // Set coordinates from selected location
      this.selectedCoordinates.set({
        latitude: location.latitude,
        longitude: location.longitude
      });
      // Clear reverse geocoded location since we're using manual selection
      this.reverseGeocodedLocation.set(null);
    }
  }

  async onCoordinatesSelected(coords: Coordinates) {
    this.selectedCoordinates.set(coords);

    // Only perform reverse geocoding if no location was manually selected
    if (!this.selectedLocation()) {
      try {
        const locationData = await this.locationSelectorService.reverseGeocode(coords.latitude, coords.longitude);
        this.reverseGeocodedLocation.set(locationData);
      } catch (error) {
        console.error('Error reverse geocoding:', error);
        this.notificationService.error('Failed to get location details', 3000);
      }
    }
  }

  onFilesChanged(files: File[]) {
    this.imageFiles.set(files);
  }

  async onSubmit() {
    // Validate form
    if (this.postForm.invalid) {
      Object.keys(this.postForm.controls).forEach(key => {
        const control = this.postForm.get(key);
        control?.markAsTouched();
      });
      this.notificationService.error('Please fill in all required fields correctly', 5000);
      return;
    }

    // Validate coordinates (location will be auto-filled via reverse geocoding)
    if (!this.selectedCoordinates()) {
      this.notificationService.error('Please select coordinates on the map', 5000);
      return;
    }

    this.isSubmitting.set(true);

    const coords = this.selectedCoordinates()!;
    const formValue = this.postForm.value;

    try {
      // Use placeId from location selector (step 1) if available
      let placeId: number;
      const manualLocation = this.selectedLocation();

      if (manualLocation) {
        // Priority 1: Use placeId from location selector (manual search)
        placeId = manualLocation.id;
      } else {
        // Priority 2: Use reverse geocoded location
        let locationData = this.reverseGeocodedLocation();
        if (!locationData) {
          // Fallback: Get location from coordinates if not already done
          locationData = await this.locationSelectorService.reverseGeocode(coords.latitude, coords.longitude);
          this.reverseGeocodedLocation.set(locationData);
        }
        placeId = locationData.placeId;
      }

      // Upload images first if any
      let imageUrls: string[] = [];
      const files = this.imageFiles();

      if (files.length > 0) {
        try {
          const uploadResults = await this.uploadsService.uploadMultipleImages(files).toPromise();
          imageUrls = uploadResults?.map(result => result.url) || [];
        } catch (error) {
          console.error('Error uploading images:', error);
          this.notificationService.error('Failed to upload images. Creating post without images.', 5000);
        }
      }

      const response = await this.postsService.createPost({
        latitude: coords.latitude,
        longitude: coords.longitude,
        title: formValue.title!,
        body: formValue.body!,
        imagesLinks: imageUrls.length > 0 ? imageUrls : undefined,
        localityId: placeId,
        localityProvider: this.locationSelectorService.getLocationProviderName() as 'google' | 'nominatim'
      }).toPromise();

      this.notificationService.success('Post created successfully!', 5000);

      // Navigate to the created post
      if (response?.id) {
        this.router.navigate(['/post', response.id]);
      } else {
        this.router.navigate(['/']);
      }
    } catch (error: any) {
      console.error('Error creating post:', error);
      const errorMessage = error?.error?.message || 'Failed to create post. Please try again.';
      this.notificationService.error(errorMessage, 5000);
    } finally {
      this.isSubmitting.set(false);
    }
  }

  get titleControl() {
    return this.postForm.get('title');
  }

  get bodyControl() {
    return this.postForm.get('body');
  }
}
