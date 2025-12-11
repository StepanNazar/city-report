import { Component, input, output, inject, ChangeDetectionStrategy, computed, signal, effect } from '@angular/core';
import { DatePipe } from '@angular/common';
import { Router } from '@angular/router';
import { EditOptions } from '../edit-options/edit-options';
import { ImageLightbox } from '../image-lightbox/image-lightbox';
import { PostResponse } from '../../services/posts.service';
import { AuthenticationService } from '../../services/authentication-service';
import { LocationSelectorService, ReverseGeocodingResult } from '../../services/location-selector-service';

@Component({
  selector: 'app-post',
  imports: [EditOptions, ImageLightbox, DatePipe],
  templateUrl: './post.html',
  styleUrl: './post.scss',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class Post {
  private authService = inject(AuthenticationService);
  private router = inject(Router);
  private locationService = inject(LocationSelectorService);

  readonly post = input.required<PostResponse>();
  readonly editClicked = output<void>();
  readonly deleteClicked = output<void>();

  readonly locationInfo = signal<ReverseGeocodingResult | null>(null);
  readonly isLoadingLocation = signal<boolean>(false);
  readonly showLightbox = signal<boolean>(false);
  readonly lightboxInitialIndex = signal<number>(0);

  readonly isAuthor = computed(() => {
    const userId = this.authService.getUserId();
    return userId !== null && this.post().authorId.toString() === userId;
  });

  constructor() {
    effect(() => {
      const postData = this.post();
      this.loadLocationInfo(postData.latitude, postData.longitude);
    });
  }

  private async loadLocationInfo(latitude: number, longitude: number) {
    this.isLoadingLocation.set(true);
    try {
      const result = await this.locationService.reverseGeocode(latitude, longitude);
      this.locationInfo.set(result);
    } catch (error) {
      console.error('Failed to load location info:', error);
      this.locationInfo.set(null);
    } finally {
      this.isLoadingLocation.set(false);
    }
  }

  onEdit() {
    this.editClicked.emit();
  }

  onDelete() {
    this.deleteClicked.emit();
  }

  navigateToAuthor() {
    this.router.navigate(['/user', this.post().authorId]);
  }

  openLightbox(index: number) {
    this.lightboxInitialIndex.set(index);
    this.showLightbox.set(true);
  }

  closeLightbox() {
    this.showLightbox.set(false);
  }
}
