import { Component } from '@angular/core';
import {
  AbstractControl,
  FormBuilder,
  FormGroup,
  Validators,
  ValidationErrors,
} from '@angular/forms';
import { RegisterRequest } from '../model/user';
import { UserService } from '../services/user-service';
import { ChangeDetectorRef } from '@angular/core';

@Component({
  selector: 'app-register',
  standalone: false,
  templateUrl: './register.html',
  styleUrl: './register.css',
})
export class Register {
  registerForm: FormGroup;
  isSubmitting = false;
  errorMessage = '';
  successMessage = '';

  constructor(
    private fb: FormBuilder,
    private userService: UserService,
    private cdr: ChangeDetectorRef,
  ) {
    this.registerForm = this.fb.group(
      {
        username: ['', [Validators.required, Validators.minLength(3)]],
        password: ['', [Validators.required, Validators.minLength(6)]],
        confirm: ['', Validators.required],
        fullname: ['', Validators.required],
      },
      {
        validators: this.passwordMatchValidator,
      },
    );
  }

  passwordMatchValidator(control: AbstractControl): ValidationErrors | null {
    const password = control.get('password')?.value;
    const confirm = control.get('confirm')?.value;

    if (!confirm) {
      return null;
    }

    return password === confirm ? null : { passwordMismatch: true };
  }

  onSubmit(): void {
    if (this.registerForm.invalid) {
      this.registerForm.markAllAsTouched();
      return;
    }

    const data: RegisterRequest = {
      username: this.registerForm.value.username,
      password: this.registerForm.value.password,
      fullname: this.registerForm.value.fullname,
    };

    this.isSubmitting = true;
    this.errorMessage = '';
    this.successMessage = '';

    this.userService.register(data).subscribe({
      next: (res) => {
        console.log('Đăng ký thành công:', res);
        this.successMessage = 'Đăng ký thành công!';
        this.registerForm.reset();
        this.isSubmitting = false;
      },
      error: (err) => {
        console.error('Lỗi đăng ký:', err);

        this.errorMessage = err.message;

        this.isSubmitting = false;
        this.cdr.detectChanges();
      },
    });
  }
}
