import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {SearchComponent} from './search/search.component';
import {DashboardComponent} from './search/dashboard/dashboard.component';
const appRoutes: Routes = [
  {
    path: 'search',
    component: SearchComponent,
  },
  {
        path: 'dashboard-result',
        component: DashboardComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(appRoutes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
