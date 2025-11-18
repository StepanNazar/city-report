import { Component, inject, OnInit, signal, ViewChild, ChangeDetectionStrategy, DestroyRef } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Router } from '@angular/router';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Subject } from 'rxjs';
import { debounceTime, switchMap } from 'rxjs/operators';
import { LocationSelector } from '../../components/location-selector/location-selector.component';
import { MapComponent } from '../../components/map/map.component';
import { ImageUpload } from '../../components/image-upload/image-upload';
import { AuthenticationService } from '../../services/authentication-service';
import { PostsService } from '../../services/posts.service';
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
  private notificationService = inject(NotificationService);
  private router = inject(Router);
  private locationSelectorService = inject(LocationSelectorService);
  private destroyRef = inject(DestroyRef);

  @ViewChild(LocationSelector) locationSelectorComponent?: LocationSelector;

  readonly isSubmitting = signal<boolean>(false);
  readonly isReverseGeocoding = signal<boolean>(false);
  readonly selectedLocation = signal<LocationOption | null>(null);
  readonly selectedCoordinates = signal<Coordinates | null>(null);
  readonly imageIds = signal<string[]>([]);
  readonly reverseGeocodedLocation = signal<ReverseGeocodingResult | null>(null);
  readonly locationSelectionError = signal<string | null>(null);

  // Subject for debouncing coordinate selection
  private coordinatesSubject = new Subject<Coordinates>();

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
      return;
    }

    // Setup debounced reverse geocoding with race condition prevention
    this.coordinatesSubject.pipe(
      debounceTime(500), // Wait 500 ms after last coordinate change
      switchMap(coords => {
        this.isReverseGeocoding.set(true);
        this.locationSelectionError.set(null);
        return this.locationSelectorService.reverseGeocode(coords.latitude, coords.longitude);
      }),
      takeUntilDestroyed(this.destroyRef)
    ).subscribe({
      next: async (locationData) => {
        this.reverseGeocodedLocation.set(locationData);
        this.isReverseGeocoding.set(false);

        // Auto-populate location selector with reverse geocoded data
        if (this.locationSelectorComponent) {
          await this.locationSelectorComponent.populateFromReverseGeocode(locationData);
        }
      },
      error: (error) => {
        console.error('Error reverse geocoding:', error);
        this.isReverseGeocoding.set(false);
        this.notificationService.error(
          'Failed to get location details. Please try selecting a different point.',
          5000
        );
      }
    });
  }

  onLocationSelected(location: LocationOption | null) {
    // Only store the selected location for its OSM ID
    // Do NOT change the map coordinates - those come from Step 1 only
    this.selectedLocation.set(location);
    if (location) {
      this.locationSelectionError.set(null);
    }
  }

  onCoordinatesSelected(coords: Coordinates) {
    this.selectedCoordinates.set(coords);
    // Emit to debounced subject - this prevents race conditions
    this.coordinatesSubject.next(coords);
  }

  onImageIdsChanged(ids: string[]) {
    this.imageIds.set(ids);
  }

  async onSubmit() {
    if (this.postForm.invalid) {
      Object.keys(this.postForm.controls).forEach(key => {
        const control = this.postForm.get(key);
        if (control?.invalid) {
          control.markAsTouched();
        }
      });
      this.notificationService.error('Please fill in all required fields correctly', 5000);
      return;
    }

    if (!this.selectedCoordinates()) {
      this.notificationService.error('Please select coordinates on the map', 5000);
      return;
    }

    if (!this.selectedLocation()) {
      this.notificationService.error('Please select a city/location from the dropdown', 5000);
      return;
    }

    if (this.isReverseGeocoding()) {
      this.notificationService.error('Please wait while we identify the location', 5000);
      return;
    }

    this.isSubmitting.set(true);

    const coords = this.selectedCoordinates()!;
    const formValue = this.postForm.value;

    try {
      // Determine OSM ID: Priority 1 is manual location selector, Priority 2 is reverse geocoded
      let osmId: number;
      const manualLocation = this.selectedLocation();

      if (manualLocation) {
        osmId = manualLocation.id;
      } else {
        const locationData = this.reverseGeocodedLocation();
        if (!locationData) {
          this.locationSelectionError.set(
            'Could not identify location from coordinates. Please use the search above to select a specific place.',
          );
          this.isSubmitting.set(false);
          return;
        }
        osmId = locationData.osmId;
      }

      const uploadedImageIds = this.imageIds();

      this.postsService.createPost({
        latitude: coords.latitude,
        longitude: coords.longitude,
        title: formValue.title!,
        body: formValue.body!,
        imagesIds: uploadedImageIds.length > 0 ? uploadedImageIds : undefined,
        localityId: osmId,
        localityProvider: this.locationSelectorService.getLocationProviderName() as 'google' | 'nominatim'
      }).pipe(
        takeUntilDestroyed(this.destroyRef)
      ).subscribe({
        next: (response) => {
          this.notificationService.success('Post created successfully!', 5000);
          this.router.navigate(['/post', response.id]);
        },
        error: (error) => {
          console.error('Error creating post:', error);
          const errorMessage = error?.error?.message || 'Failed to create post. Please try again.';
          this.notificationService.error(errorMessage, 5000);
          this.isSubmitting.set(false);
        }
      });
    } catch (error: any) {
      console.error('Error creating post:', error);
      const errorMessage = error?.error?.message || 'Failed to create post. Please try again.';
      this.notificationService.error(errorMessage, 5000);
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
