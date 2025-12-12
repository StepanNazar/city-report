import { Component, input, inject, ChangeDetectionStrategy } from '@angular/core';
import { Router } from '@angular/router';
import { PostResponse } from '../../services/posts.service';
import { DatePipe } from '@angular/common';

@Component({
  selector: 'app-short-post-info',
  imports: [DatePipe],
  templateUrl: './short-post-info.html',
  styleUrl: './short-post-info.scss',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ShortPostInfo {
  private router = inject(Router);

  post = input.required<PostResponse>();

  navigateToPost() {
    this.router.navigate(['/post', this.post().id]);
  }
}
