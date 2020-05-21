import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { BaseComponent } from '../../base/base.component';
import { UserService } from '../../../service/user.service';
import { UserData } from '../../../model/userData';
import { Validators, FormGroup, FormBuilder, FormControl, NgForm } from '@angular/forms';
import { HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'app-user-form',
  templateUrl: './user-form.component.html',
  styleUrls: ['./user-form.component.css']
})
export class UserFormComponent extends BaseComponent implements OnInit {
  id: string;
  userData: UserData;
  submitted: boolean;
  form: FormGroup;

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private route: ActivatedRoute,
    public userService: UserService
  ) { super(); }

  ngOnInit() {
    this.userData = new UserData();
    this.form = this.fb.group({
      'Id': [null],
      'UserName': [null, Validators.required],
      'FirstName': [null, Validators.required],
      'Password': [null, Validators.required],
      'UserType': [null, Validators.required]
    });

    this.safeSub(
      this.route.paramMap.subscribe(params => {
        if (params.has('id')) {
          this.safeSub(
            this.userService.getById(params.get('id')).subscribe((userData: UserData) => {
              this.userData = userData;
              this.form.patchValue(this.userData);
            })
          );
        }
      })
    );
  }

  onFormSubmit = (form: NgForm) => {
    this.submitted = true;
    if (!this.form.valid) {
      return;
    }
    this.userData = this.form.value as UserData;
    this.userService.save(this.userData).subscribe(
      () => {
        this.userService.refresh();
        this.router.navigateByUrl('/users/list');
      },
      (error: HttpErrorResponse) => {
        console.error(error);
      });
  }

  prepareForm() {
    this.form = new FormGroup({
      Id: new FormControl(''),
      UserName: new FormControl('', Validators.required),
      FirstName: new FormControl('', Validators.required),
      Password: new FormControl('', Validators.required),
      UserType: new FormControl('', Validators.required)
    });
  }
}
