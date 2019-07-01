import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { SittersListComponent } from './sitters-list/sitters-list.component';

const routes: Routes = [
  { path: '', redirectTo: 'sitter', pathMatch: 'full' },
  { path: 'sitter', component: SittersListComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})

export class AppRoutingModule { }
