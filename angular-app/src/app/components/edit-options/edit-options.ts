import { Component, output, ChangeDetectionStrategy } from '@angular/core';

@Component({
  selector: 'app-edit-options',
  imports: [],
  templateUrl: './edit-options.html',
  styleUrl: './edit-options.scss',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class EditOptions {
  readonly editClicked = output<void>();
  readonly deleteClicked = output<void>();

  onEdit() {
    this.editClicked.emit();
  }

  onDelete() {
    this.deleteClicked.emit();
  }
}
