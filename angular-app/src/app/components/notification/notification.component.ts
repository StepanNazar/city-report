import { Component, inject, ChangeDetectionStrategy } from '@angular/core';
import { NotificationService } from '../../services/notification.service';

@Component({
  selector: 'app-notification',
  imports: [],
  templateUrl: './notification.component.html',
  styleUrl: './notification.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class NotificationComponent {
  notificationService = inject(NotificationService);
}

