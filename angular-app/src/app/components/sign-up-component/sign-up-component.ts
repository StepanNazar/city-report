import {Component, inject} from '@angular/core';
import { LocationSelector } from '../location-selector/location-selector.component';
import {FormControl, FormGroup, ReactiveFormsModule, Validators} from '@angular/forms';
import {HttpClient} from '@angular/common/http';
import {AuthenticationService} from '../../services/authentication-service';
import {passwordMatchValidator, passwordPatternValidator} from '../../validators/password.validator';

interface AccessTokenResponse {
  access_token: string;
}

@Component({
  selector: 'app-sign-up-component',
  imports: [LocationSelector, ReactiveFormsModule],
  templateUrl: './sign-up-component.html',
  styleUrl: './sign-up-component.scss'
})
export class SignUpComponent {
  http = inject(HttpClient);
  authService = inject(AuthenticationService);

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
      next: (response) => {
        // Handle success
      },
      error: (error) => {
        console.log(`${error.statusText} ${error?.error?.message || ''}`);
      }
    });
  }
}
