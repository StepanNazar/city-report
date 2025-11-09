import {Component, inject} from '@angular/core';
import { Router } from '@angular/router';
import {FormControl, FormGroup, ReactiveFormsModule, Validators} from '@angular/forms';
import {HttpClient} from '@angular/common/http';
import {AuthenticationService} from '../../services/authentication-service';
import { NotificationService } from '../../services/notification.service';
import {passwordMatchValidator, passwordPatternValidator} from '../../validators/password.validator';

@Component({
  selector: 'app-sign-up-component',
  imports: [ReactiveFormsModule],
  templateUrl: './sign-up-component.html',
  styleUrl: './sign-up-component.scss'
})
export class SignUpComponent {
  http = inject(HttpClient);
  authService = inject(AuthenticationService);
  notificationService = inject(NotificationService);
  router = inject(Router);

  loginForm: FormGroup = new FormGroup({
    firstName: new FormControl('', [Validators.required]),
    lastName: new FormControl('', [Validators.required]),
    email: new FormControl('', [Validators.required, Validators.email]),
    password: new FormControl('', [
      Validators.required,
      Validators.minLength(8),
      Validators.maxLength(128),
      passwordPatternValidator()
    ]),
    confirmPassword: new FormControl('', [Validators.required]),
    // locality_id: new FormControl(''),
  }, { validators: passwordMatchValidator() });

  onSubmit() {
    if (this.loginForm.invalid) {
      Object.values(this.loginForm.controls).forEach(control => control.markAsTouched());
      return;
    }
    const payload = this.loginForm.value;
    delete payload.confirmPassword;
    this.authService.register(payload).subscribe({
      next: () => {
        this.notificationService.success('Account created successfully! Welcome to City Report.');
        this.router.navigate(['/']);
      },
      error: (error) => {
        const message = error?.error?.message || error.statusText || 'An error occurred during registration';
        this.notificationService.error(message);
      }
    });
  }
}
