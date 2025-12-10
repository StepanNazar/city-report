import { Component, input, output, OnInit, signal, ChangeDetectionStrategy } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { ImageUpload } from '../image-upload/image-upload';
import { SolutionResponse } from '../../services/solutions.service';

@Component({
  selector: 'app-solution-edit',
  imports: [ReactiveFormsModule, ImageUpload],
  templateUrl: './solution-edit.html',
  styleUrl: './solution-edit.scss',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class SolutionEdit implements OnInit {
  readonly solution = input<SolutionResponse | null>(null);
  readonly saveClicked = output<{
    title: string;
    body: string;
    imagesIds?: string[];
  }>();
  readonly cancelClicked = output<void>();

  readonly imageIds = signal<string[]>([]);

  solutionForm = new FormGroup({
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
    const solutionData = this.solution();
    if (solutionData) {
      this.solutionForm.patchValue({
        title: solutionData.title,
        body: solutionData.body
      });

      // Extract image IDs from images array
      if (solutionData.images && solutionData.images.length > 0) {
        const ids = solutionData.images.map(img => img.id);
        this.imageIds.set(ids);
      }
    }
  }

  onImageIdsChanged(ids: string[]) {
    this.imageIds.set(ids);
  }

  onSave() {
    if (this.solutionForm.invalid) {
      Object.keys(this.solutionForm.controls).forEach(key => {
        const control = this.solutionForm.get(key);
        if (control?.invalid) {
          control.markAsTouched();
        }
      });
      return;
    }

    const formValue = this.solutionForm.value;
    this.saveClicked.emit({
      title: formValue.title!,
      body: formValue.body!,
      imagesIds: this.imageIds().length > 0 ? this.imageIds() : undefined
    });
  }

  onCancel() {
    this.cancelClicked.emit();
  }

  get titleControl() {
    return this.solutionForm.get('title');
  }

  get bodyControl() {
    return this.solutionForm.get('body');
  }
}
