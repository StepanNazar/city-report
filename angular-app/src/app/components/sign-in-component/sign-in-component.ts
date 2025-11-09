import { Component, inject } from '@angular/core';
import {FormControl, FormGroup, ReactiveFormsModule, Validators} from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { AuthenticationService } from '../../services/authentication-service';
import {passwordPatternValidator} from '../../validators/password.validator';

@Component({
  selector: 'app-sign-in-component',
  imports: [ReactiveFormsModule],
  templateUrl: './sign-in-component.html',
  styleUrl: './sign-in-component.scss'
})
export class SignInComponent {
  http = inject(HttpClient);
  authService = inject(AuthenticationService);

  loginForm: FormGroup = new FormGroup({
    email: new FormControl('', [Validators.required, Validators.email]),
    password: new FormControl('', [
      Validators.required,
      Validators.minLength(8),
      Validators.maxLength(128),
      passwordPatternValidator()
    ]),
  });

  onSubmit() {
    if (this.loginForm.invalid) {
      Object.values(this.loginForm.controls).forEach(control => control.markAsTouched());
      return;
    }
    const payload = this.loginForm.value;
    this.authService.login(payload).subscribe({
      next: (response) => {
        // Handle success
      },
      error: (error) => {
        console.log(`${error.statusText} ${error?.error?.message || ''}`);
      }
    });
  }
}
