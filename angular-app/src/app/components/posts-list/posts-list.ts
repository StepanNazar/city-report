import { Component, inject, input, OnChanges, SimpleChanges, signal } from '@angular/core';
import { ShortPostInfo } from '../short-post-info/short-post-info';
import { PostResponse, PostsService } from '../../services/posts.service';
import { LocationOption, LocationSelectorService } from '../../services/location-selector-service';

@Component({
  selector: 'app-posts-list',
  imports: [ShortPostInfo],
  templateUrl: './posts-list.html',
  styleUrl: './posts-list.scss'
})
export class PostsList implements OnChanges {
  private postsService = inject(PostsService);
  private locationSelectorService = inject(LocationSelectorService);

  location = input<LocationOption | null>();
  sortBy = input<string>('createdAt');
  order = input<string>('desc');

  readonly posts = signal<PostResponse[]>([]);
  readonly isLoading = signal<boolean>(false);
  readonly error = signal<string | null>(null);
  readonly currentPage = signal<number>(1);
  readonly totalPages = signal<number>(0);
  readonly hasPrev = signal<boolean>(false);
  readonly hasNext = signal<boolean>(false);

  ngOnChanges(changes: SimpleChanges) {
    // Reset page to 1 when location, sortBy, or order changes
    if (changes['location'] || changes['sortBy'] || changes['order']) {
      this.currentPage.set(1);
      this.fetchPosts();
    }
  }

  goToPage(page: number) {
    if (page >= 1 && page <= this.totalPages()) {
      this.currentPage.set(page);
      this.fetchPosts();
    }
  }

  nextPage() {
    if (this.hasNext()) {
      this.goToPage(this.currentPage() + 1);
    }
  }

  prevPage() {
    if (this.hasPrev()) {
      this.goToPage(this.currentPage() - 1);
    }
  }

  private fetchPosts() {
    this.isLoading.set(true);
    this.error.set(null);
    const location = this.location();
    this.postsService.getPosts(
      location?.id,
      this.locationSelectorService.locationProviderName,
      this.currentPage(),
      10,
      this.sortBy(),
      this.order()
    ).subscribe({
      next: (response) => {
        this.posts.set(response.items);
        this.currentPage.set(response.page);
        this.totalPages.set(response.totalPages);
        this.hasPrev.set(response.hasPrev);
        this.hasNext.set(response.hasNext);
        this.isLoading.set(false);
      },
      error: (err) => {
        this.error.set('Error loading posts');
        this.isLoading.set(false);
      }
    });
  }
}
