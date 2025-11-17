import { Component, inject, OnInit, signal, ViewChild, ChangeDetectionStrategy } from '@angular/core';
import { Router } from '@angular/router';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { LocationSelector } from '../../components/location-selector/location-selector.component';
import { MapComponent } from '../../components/map/map.component';
import { ImageUpload } from '../../components/image-upload/image-upload';
import { AuthenticationService } from '../../services/authentication-service';
import { PostsService } from '../../services/posts.service';
import { UploadsService } from '../../services/uploads.service';
import { NotificationService } from '../../services/notification.service';
import { LocationOption, LocationSelectorService, ReverseGeocodingResult } from '../../services/location-selector-service';
import {Coordinates} from '../../services/geolocation.service';

@Component({
  selector: 'app-create-post-page',
  imports: [LocationSelector, MapComponent, ImageUpload, ReactiveFormsModule],
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
  @ViewChild(LocationSelector) locationSelectorComponent?: LocationSelector;

  readonly isSubmitting = signal<boolean>(false);
  readonly selectedLocation = signal<LocationOption | null>(null);
  readonly selectedCoordinates = signal<Coordinates | null>(null);
  readonly imageIds = signal<string[]>([]);
  readonly reverseGeocodedLocation = signal<ReverseGeocodingResult | null>(null);
  readonly locationSelectionError = signal<string | null>(null);

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
    // Only store the selected location for its OSM ID
    // Do NOT change the map coordinates - those come from Step 1 only
    this.selectedLocation.set(location);
  }

  async onCoordinatesSelected(coords: Coordinates) {
    this.selectedCoordinates.set(coords);

    // Always perform reverse geocoding when coordinates are selected
    try {
      const locationData = await this.locationSelectorService.reverseGeocode(coords.latitude, coords.longitude);
      this.reverseGeocodedLocation.set(locationData);
      this.locationSelectionError.set(null);

      // Auto-populate location selector (Step 2) with reverse geocoded data
      if (this.locationSelectorComponent) {
        await this.locationSelectorComponent.populateFromReverseGeocode(locationData);
      }
    } catch (error) {
      console.error('Error reverse geocoding:', error);
      this.notificationService.error('Failed to get location details', 3000);
      this.locationSelectionError.set('Failed to retrieve location details. Please try selecting a different point.');
    }
  }

  onImageIdsChanged(ids: string[]) {
    this.imageIds.set(ids);
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

    // Validate coordinates
    if (!this.selectedCoordinates()) {
      this.notificationService.error('Please select coordinates on the map', 5000);
      return;
    }

    this.isSubmitting.set(true);

    const coords = this.selectedCoordinates()!;
    const formValue = this.postForm.value;

    try {
      // Determine place ID: Priority 1 is manual location selector, Priority 2 is reverse geocoded
      let placeId: number;
      const manualLocation = this.selectedLocation();

      if (manualLocation) {
        // User manually selected a location from search
        placeId = manualLocation.id;
      } else {
        // Use reverse geocoded location
        let locationData = this.reverseGeocodedLocation();
        if (!locationData) {
          // Fallback: Get location from coordinates if not already done
          try {
            locationData = await this.locationSelectorService.reverseGeocode(coords.latitude, coords.longitude);
            this.reverseGeocodedLocation.set(locationData);
          } catch (error) {
            console.error('Error getting location:', error);
            this.notificationService.error(
              'Failed to identify location. Please use the location search to select a specific place.',
              5000
            );
            this.locationSelectionError.set(
              'Could not identify location from coordinates. Please use the search above to select a specific place.'
            );
            this.isSubmitting.set(false);
            return;
          }
        }
        placeId = locationData.placeId;
      }

      // Get uploaded image IDs
      const uploadedImageIds = this.imageIds();

      const response = await this.postsService.createPost({
        latitude: coords.latitude,
        longitude: coords.longitude,
        title: formValue.title!,
        body: formValue.body!,
        imagesIds: uploadedImageIds.length > 0 ? uploadedImageIds : undefined,
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
