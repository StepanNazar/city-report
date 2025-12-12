import { Component, input, output, inject, computed, ChangeDetectionStrategy } from '@angular/core';
import { DatePipe } from '@angular/common';
import { Router } from '@angular/router';
import { SolutionResponse } from '../../services/solutions.service';
import { AuthenticationService } from '../../services/authentication-service';
import { EditOptions } from '../edit-options/edit-options';

@Component({
  selector: 'app-solution',
  imports: [DatePipe, EditOptions],
  templateUrl: './solution.html',
  styleUrl: './solution.scss',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class Solution {
  private authService = inject(AuthenticationService);
  private router = inject(Router);

  readonly solution = input.required<SolutionResponse>();
  readonly isPostAuthor = input<boolean>(false);
  readonly editClicked = output<void>();
  readonly deleteClicked = output<void>();
  readonly approveClicked = output<void>();
  readonly removeApprovalClicked = output<void>();

  readonly isAuthor = computed(() => {
    const userId = this.authService.getUserId();
    return userId !== null && this.solution().authorId.toString() === userId;
  });

  onEdit() {
    this.editClicked.emit();
  }

  onDelete() {
    this.deleteClicked.emit();
  }

  onApprove() {
    this.approveClicked.emit();
  }

  onRemoveApproval() {
    this.removeApprovalClicked.emit();
  }

  navigateToAuthor() {
    this.router.navigate(['/user', this.solution().authorId]);
  }
}
