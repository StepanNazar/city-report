import { Component, input, output, inject, OnInit, signal, ChangeDetectionStrategy, viewChild } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { ImageEdit } from '../image-edit/image-edit';
import { LocationSelector } from '../location-selector/location-selector.component';
import { PostResponse } from '../../services/posts.service';
import { LocationOption, LocationSelectorService } from '../../services/location-selector-service';

@Component({
  selector: 'app-post-edit',
  imports: [ImageEdit, LocationSelector, ReactiveFormsModule],
  templateUrl: './post-edit.html',
  styleUrl: './post-edit.scss',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class PostEdit implements OnInit {
  private locationService = inject(LocationSelectorService);

  readonly post = input.required<PostResponse>();
  readonly saveClicked = output<{
    title: string;
    body: string;
    latitude: number;
    longitude: number;
    localityId: number;
    localityProvider: 'nominatim' | 'google';
    imagesIds?: string[];
  }>();
  readonly cancelClicked = output<void>();

  readonly imageIds = signal<string[]>([]);
  readonly selectedLocation = signal<LocationOption | null>(null);
  readonly locationSelector = viewChild<LocationSelector>('locationSelector');
  readonly isLoadingLocation = signal<boolean>(false);

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
    ]),
    latitude: new FormControl<number | null>(null, [Validators.required]),
    longitude: new FormControl<number | null>(null, [Validators.required])
  });

  async ngOnInit() {
    const postData = this.post();
    this.postForm.patchValue({
      title: postData.title,
      body: postData.body,
      latitude: postData.latitude,
      longitude: postData.longitude
    });

    // Load location data for the current coordinates
    await this.loadLocationForCoordinates(postData.latitude, postData.longitude);
  }

  private async loadLocationForCoordinates(latitude: number, longitude: number) {
    this.isLoadingLocation.set(true);
    try {
      const result = await this.locationService.reverseGeocode(latitude, longitude);
      const selector = this.locationSelector();
      if (selector) {
        await selector.populateFromReverseGeocode(result);
      }
    } catch (error) {
      console.error('Failed to load location for coordinates:', error);
    } finally {
      this.isLoadingLocation.set(false);
    }
  }

  onImageIdsChanged(ids: string[]) {
    this.imageIds.set(ids);
  }

  onLocationSelected(location: LocationOption | null) {
    this.selectedLocation.set(location);
  }

  onSave() {
    if (this.postForm.invalid) {
      Object.keys(this.postForm.controls).forEach(key => {
        const control = this.postForm.get(key);
        if (control?.invalid) {
          control.markAsTouched();
        }
      });
      return;
    }

    const formValue = this.postForm.value;
    const postData = this.post();
    const location = this.selectedLocation();

    // Use updated coordinates from form or fall back to original
    const latitude = formValue.latitude ?? postData.latitude;
    const longitude = formValue.longitude ?? postData.longitude;

    this.saveClicked.emit({
      title: formValue.title!,
      body: formValue.body!,
      latitude: latitude,
      longitude: longitude,
      localityId: location?.id ?? postData.localityNominatimId ?? 0,
      localityProvider: 'nominatim',
      imagesIds: this.imageIds().length > 0 ? this.imageIds() : undefined
    });
  }

  async onCoordinatesChanged() {
    const latitude = this.postForm.get('latitude')?.value;
    const longitude = this.postForm.get('longitude')?.value;

    if (latitude !== null && longitude !== null && latitude !== undefined && longitude !== undefined) {
      await this.loadLocationForCoordinates(latitude, longitude);
    }
  }

  onCancel() {
    this.cancelClicked.emit();
  }

  get titleControl() {
    return this.postForm.get('title');
  }

  get bodyControl() {
    return this.postForm.get('body');
  }
}
