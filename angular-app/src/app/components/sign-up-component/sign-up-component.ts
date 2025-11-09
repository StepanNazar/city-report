import {Component, inject} from '@angular/core';
import { LocationSelector } from '../location-selector/location-selector.component';
import {
  AbstractControl,
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  ValidationErrors,
  ValidatorFn,
  Validators
} from '@angular/forms';
import {HttpClient} from '@angular/common/http';
import {AuthenticationService} from '../../services/authentication-service';

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
      this.passwordPatternValidator()
    ]),
    confirmPassword: new FormControl('', [Validators.required]),
    // locality_id: new FormControl(''),
  }, { validators: this.passwordMatchValidator() });

  passwordPatternValidator(): ValidatorFn {
    return (control: AbstractControl): ValidationErrors | null => {
      const value = control.value;
      if (!value) {
        return null;
      }

      const hasDigit = /\d/.test(value);
      const hasUppercase = /[A-Z]/.test(value);
      const hasLowercase = /[a-z]/.test(value);
      const hasSpecial = /\W/.test(value);

      const valid = hasDigit && hasUppercase && hasLowercase && hasSpecial;

      return valid ? null : { pattern: true };
    };
  }

  passwordMatchValidator(): ValidatorFn {
    return (control: AbstractControl): ValidationErrors | null => {
      const password = control.get('password');
      const confirmPassword = control.get('confirmPassword');

      if (!password || !confirmPassword) {
        return null;
      }

      return password.value === confirmPassword.value ? null : { passwordMismatch: true };
    };
  }

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
