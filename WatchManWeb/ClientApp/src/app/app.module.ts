import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { RouterModule } from '@angular/router';

import { AppComponent } from './app.component';
import { NavMenuComponent } from './component/nav-menu/nav-menu.component';
import { HomeComponent } from './component/home/home.component';
import { LoginComponent } from './component/login/login.component';
import { MonitoringComponent } from './component/monitoring/monitoring.component';
import { AnalysisComponent } from './component/analysis/analysis.component';

import { HttpInterceptorService } from './service/http-interceptor.service';
import { ErrorInterceptorService } from './service/error-interceptor.service';

import { AuthGuard } from './guards/auth.guard';
import { ReportsComponent } from './component/reports/reports.component';
import { UserFormComponent } from './component/user/user-form/user-form.component';
import { UserListComponent } from './component/user/user-list/user-list.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';


@NgModule({
  declarations: [
    AppComponent,
    NavMenuComponent,
    HomeComponent,
    LoginComponent,
    MonitoringComponent,
    AnalysisComponent,
    ReportsComponent,
    UserFormComponent,
    UserListComponent
  ],
  imports: [
    BrowserModule.withServerTransition({ appId: 'ng-cli-universal' }),
    BrowserAnimationsModule,
    TableModule,
    ButtonModule,
    InputTextModule,
    HttpClientModule,
    ReactiveFormsModule,
    RouterModule.forRoot([
      { path: '', component: HomeComponent, pathMatch: 'full' },
      { path: 'login', component: LoginComponent },
      { path: 'monitoring', component: MonitoringComponent },
      { path: 'analysis', component: AnalysisComponent, canActivate: [AuthGuard] }, 
      { path: 'reports', component: ReportsComponent, canActivate: [AuthGuard] },
      {
        path: 'users',
        canActivate: [AuthGuard],
        children: [
          {
            path: 'list',
            pathMatch: 'full',
            component: UserListComponent
          },
          {
            path: 'details/:id',
            component: UserFormComponent
          },
          {
            path: 'details',
            component: UserFormComponent
          },
          { path: '', redirectTo: 'list', pathMatch: 'full' }
        ]
      },
    ])
  ],
  providers: [{ provide: HTTP_INTERCEPTORS, useClass: HttpInterceptorService, multi: true },
  { provide: HTTP_INTERCEPTORS, useClass: ErrorInterceptorService, multi: true },
  ], 
  bootstrap: [AppComponent]
})
export class AppModule { }
