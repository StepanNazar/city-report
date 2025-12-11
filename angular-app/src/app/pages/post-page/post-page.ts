import { Component, inject, signal, OnInit, ChangeDetectionStrategy, DestroyRef } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { Post } from '../../components/post/post';
import { PostEdit } from '../../components/post-edit/post-edit';
import { Solutions } from '../../components/solutions/solutions';
import { AIComment } from '../../components/aicomment/aicomment';
import { Comments } from '../../components/comments/comments';
import { PostsService, PostResponse } from '../../services/posts.service';
import { NotificationService } from '../../services/notification.service';

@Component({
  selector: 'app-post-page',
  imports: [Post, PostEdit, Solutions, AIComment, Comments, RouterLink],
  templateUrl: './post-page.html',
  styleUrl: './post-page.scss',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class PostPage implements OnInit {
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private postsService = inject(PostsService);
  private notificationService = inject(NotificationService);
  private destroyRef = inject(DestroyRef);

  readonly post = signal<PostResponse | null>(null);
  readonly isLoading = signal<boolean>(true);
  readonly isEditing = signal<boolean>(false);

  ngOnInit() {
    this.route.params.pipe(
      takeUntilDestroyed(this.destroyRef)
    ).subscribe(params => {
      const postId = +params['id'];
      if (postId) {
        this.loadPost(postId);
      }
    });
  }

  loadPost(postId: number) {
    this.isLoading.set(true);
    this.postsService.getPost(postId).pipe(
      takeUntilDestroyed(this.destroyRef)
    ).subscribe({
      next: (response) => {
        this.post.set(response);
        this.isLoading.set(false);
      },
      error: (error) => {
        console.error('Error loading post:', error);
        this.notificationService.error('Failed to load post', 5000);
        this.isLoading.set(false);
        this.router.navigate(['/']);
      }
    });
  }

  startEditPost() {
    this.isEditing.set(true);
  }

  cancelEditPost() {
    this.isEditing.set(false);
  }

  updatePost(data: {
    title: string;
    body: string;
    latitude: number;
    longitude: number;
    localityId: number;
    localityProvider: 'nominatim' | 'google';
    imagesIds?: string[];
  }) {
    const currentPost = this.post();
    if (!currentPost) return;

    this.postsService.updatePost(currentPost.id, data).pipe(
      takeUntilDestroyed(this.destroyRef)
    ).subscribe({
      next: (response) => {
        this.post.set(response);
        this.isEditing.set(false);
        this.notificationService.success('Post updated successfully!', 5000);
      },
      error: (error) => {
        console.error('Error updating post:', error);
        const errorMessage = error?.error?.message || 'Failed to update post';
        this.notificationService.error(errorMessage, 5000);
      }
    });
  }

  deletePost() {
    const currentPost = this.post();
    if (!currentPost) return;

    if (!confirm('Are you sure you want to delete this post? This action cannot be undone.')) {
      return;
    }

    this.postsService.deletePost(currentPost.id).pipe(
      takeUntilDestroyed(this.destroyRef)
    ).subscribe({
      next: () => {
        this.notificationService.success('Post deleted successfully!', 5000);
        this.router.navigate(['/']);
      },
      error: (error) => {
        console.error('Error deleting post:', error);
        const errorMessage = error?.error?.message || 'Failed to delete post';
        this.notificationService.error(errorMessage, 5000);
      }
    });
  }
}
