import { Component, OnInit, OnDestroy } from '@angular/core';
import { UserService } from '../../../service/user.service';
import { UserData } from '../../../model/userData';
import { BaseComponent } from '../../base/base.component';

@Component({
  selector: 'app-user-list',
  templateUrl: './user-list.component.html',
  styleUrls: ['./user-list.component.css']
})

export class UserListComponent extends BaseComponent implements OnInit {

  users: UserData[] = [];
  cols: any[];

  constructor(
    public userService: UserService) { super();}



  ngOnInit() {
    this.safeSub(
      this.userService.getAll().subscribe(
        (users) => {
          this.users = users;
        }
      )
    );

    this.cols = [
      { field: 'userName', header: 'Username' },
      { field: 'type', header: 'Type' },
    ];
  }


  //remove(id: string) {
  //  this.safeSub(
  //    this.userService.delete(id).subscribe(
  //      () => {
  //        this.userService.refresh();
  //      })
  //  );
  //}

}
