import { Component, input, inject, signal, computed, effect, ChangeDetectionStrategy, DestroyRef } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Solution } from '../solution/solution';
import { SolutionEdit } from '../solution-edit/solution-edit';
import { SolutionsService, SolutionResponse } from '../../services/solutions.service';
import { NotificationService } from '../../services/notification.service';
import { AuthenticationService } from '../../services/authentication-service';

@Component({
  selector: 'app-solutions',
  imports: [Solution, SolutionEdit],
  templateUrl: './solutions.html',
  styleUrl: './solutions.scss',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class Solutions {
  private solutionsService = inject(SolutionsService);
  private notificationService = inject(NotificationService);
  private authService = inject(AuthenticationService);
  private destroyRef = inject(DestroyRef);

  readonly postId = input.required<number>();
  readonly postAuthorId = input.required<number>();

  readonly solutions = signal<SolutionResponse[]>([]);
  readonly currentPage = signal<number>(1);
  readonly totalPages = signal<number>(1);
  readonly totalItems = signal<number>(0);
  readonly isLoading = signal<boolean>(false);
  readonly sortBy = signal<string>('likes');
  readonly order = signal<string>('desc');
  readonly onlyApproved = signal<boolean>(false);
  readonly showCreateForm = signal<boolean>(false);
  readonly editingSolutionId = signal<number | null>(null);

  readonly isPostAuthor = computed(() => {
    const userId = this.authService.getUserId();
    return userId !== null && this.postAuthorId().toString() === userId;
  });

  readonly editingSolution = computed(() => {
    const id = this.editingSolutionId();
    if (id === null) return null;
    return this.solutions().find(s => s.id === id) || null;
  });

  constructor() {
    effect(() => {
      this.loadSolutions();
    });
  }

  loadSolutions() {
    this.isLoading.set(true);
    this.solutionsService.getSolutions(
      this.postId(),
      this.currentPage(),
      5,
      this.sortBy(),
      this.order(),
      this.onlyApproved() || undefined
    ).pipe(
      takeUntilDestroyed(this.destroyRef)
    ).subscribe({
      next: (response) => {
        this.solutions.set(response.items);
        this.totalPages.set(response.totalPages);
        this.totalItems.set(response.totalItems);
        this.isLoading.set(false);
      },
      error: (error) => {
        console.error('Error loading solutions:', error);
        this.notificationService.error('Failed to load solutions', 5000);
        this.isLoading.set(false);
      }
    });
  }

  onSortChange(event: Event) {
    const select = event.target as HTMLSelectElement;
    this.sortBy.set(select.value);
    this.currentPage.set(1);
    this.loadSolutions();
  }

  onApprovedFilterChange(event: Event) {
    const checkbox = event.target as HTMLInputElement;
    this.onlyApproved.set(checkbox.checked);
    this.currentPage.set(1);
    this.loadSolutions();
  }

  goToPage(page: number) {
    if (page < 1 || page > this.totalPages()) return;
    this.currentPage.set(page);
    this.loadSolutions();
  }

  startCreateSolution() {
    if (!this.authService.isAuthenticated()) {
      this.notificationService.error('You must be logged in to create a solution', 5000);
      return;
    }
    this.showCreateForm.set(true);
  }

  cancelCreateSolution() {
    this.showCreateForm.set(false);
  }

  createSolution(data: { title: string; body: string; imagesIds?: string[] }) {
    this.solutionsService.createSolution(this.postId(), data).pipe(
      takeUntilDestroyed(this.destroyRef)
    ).subscribe({
      next: () => {
        this.notificationService.success('Solution created successfully!', 5000);
        this.showCreateForm.set(false);
        this.loadSolutions();
      },
      error: (error) => {
        console.error('Error creating solution:', error);
        const errorMessage = error?.error?.message || 'Failed to create solution';
        this.notificationService.error(errorMessage, 5000);
      }
    });
  }

  startEditSolution(solutionId: number) {
    this.editingSolutionId.set(solutionId);
  }

  cancelEditSolution() {
    this.editingSolutionId.set(null);
  }

  updateSolution(data: { title: string; body: string; imagesIds?: string[] }) {
    const solutionId = this.editingSolutionId();
    if (solutionId === null) return;

    this.solutionsService.updateSolution(solutionId, data).pipe(
      takeUntilDestroyed(this.destroyRef)
    ).subscribe({
      next: () => {
        this.notificationService.success('Solution updated successfully!', 5000);
        this.editingSolutionId.set(null);
        this.loadSolutions();
      },
      error: (error) => {
        console.error('Error updating solution:', error);
        const errorMessage = error?.error?.message || 'Failed to update solution';
        this.notificationService.error(errorMessage, 5000);
      }
    });
  }

  deleteSolution(solutionId: number) {
    if (!confirm('Are you sure you want to delete this solution?')) {
      return;
    }

    this.solutionsService.deleteSolution(solutionId).pipe(
      takeUntilDestroyed(this.destroyRef)
    ).subscribe({
      next: () => {
        this.notificationService.success('Solution deleted successfully!', 5000);
        this.loadSolutions();
      },
      error: (error) => {
        console.error('Error deleting solution:', error);
        const errorMessage = error?.error?.message || 'Failed to delete solution';
        this.notificationService.error(errorMessage, 5000);
      }
    });
  }

  approveSolution(solutionId: number) {
    console.log('Approve solution:', solutionId);
    this.notificationService.info('Approve solution feature coming soon', 3000);
  }
}
