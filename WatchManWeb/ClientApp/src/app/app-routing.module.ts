import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from './guards/auth.guard';

import { HomeComponent } from './component/home/home.component';
import { LoginComponent } from './component/login/login.component';
import { MonitoringComponent } from './component/monitoring/monitoring.component';
import { AnalysisComponent } from './component/analysis/analysis.component';
import { ReportsComponent } from './component/reports/reports.component';
import { UserFormComponent } from './component/user/user-form/user-form.component';
import { UserListComponent } from './component/user/user-list/user-list.component';

const routes: Routes = [
    { path: '', component: HomeComponent, pathMatch: 'full' },
    { path: 'login', component: LoginComponent },
    { path: 'monitoring', component: MonitoringComponent, canActivate: [AuthGuard] },
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
    }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
  declarations: []
})
export class AppRoutingModule { }