import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, UrlTree, Router } from '@angular/router';
import { Observable } from 'rxjs';
import { AuthService } from '../service/auth.service';
import { User } from '../model/user';
import { UserRole } from '../enum/roles';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {
  userDataSubscription: any;
  userData = new User();
  constructor(private router: Router, private authService: AuthService) {
    this.userDataSubscription = this.authService.userData.asObservable().subscribe(data => {
      this.userData = data;
    });
  }
  canActivate(
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {
    
    if (this.userData.isLoggedIn === true) {

      if (this.userData.role == UserRole.Admin)
        return true;

      if (this.userData.role == UserRole.AdvancedUser && !this.checkAdminUrl(state)) 
        return true;

      if (!this.checkAdvancedUrl(state) && !this.checkAdminUrl(state))
        return true;
      
      this.router.navigate(['/']);
      return false;
    }

    this.router.navigate(['/login'], { queryParams: { returnUrl: state.url } });
    return false;
  }

  checkAdvancedUrl(state) {
    return state.url === '/analysis' || state.url === '/reports';
  }

  checkAdminUrl(state) {
    return state.url.startsWith('/users');
  }
}
