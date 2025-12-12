import { Component, input, output, inject, OnInit, signal, ChangeDetectionStrategy } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { ImageUpload } from '../image-upload/image-upload';
import { LocationSelector } from '../location-selector/location-selector.component';
import { PostResponse } from '../../services/posts.service';
import { LocationOption } from '../../services/location-selector-service';

@Component({
  selector: 'app-post-edit',
  imports: [ImageUpload, LocationSelector, ReactiveFormsModule],
  templateUrl: './post-edit.html',
  styleUrl: './post-edit.scss',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class PostEdit implements OnInit {
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

  ngOnInit() {
    const postData = this.post();
    this.postForm.patchValue({
      title: postData.title,
      body: postData.body,
      latitude: postData.latitude,
      longitude: postData.longitude
    });

    // Extract image IDs from images array
    if (postData.images && postData.images.length > 0) {
      const ids = postData.images.map(img => img.id);
      this.imageIds.set(ids);
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

    this.saveClicked.emit({
      title: formValue.title!,
      body: formValue.body!,
      latitude: formValue.latitude ?? postData.latitude,
      longitude: formValue.longitude ?? postData.longitude,
      localityId: location?.id ?? postData.localityNominatimId ?? 0,
      localityProvider: 'nominatim',
      imagesIds: this.imageIds().length > 0 ? this.imageIds() : undefined
    });
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
