import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
// import { AppComponent } from './app.component_OLEG';
import { AppComponent } from './app.component';
import { RatingComponent } from './rating/rating.component';
import { SittersListComponent } from './sitters-list/sitters-list.component';
import { SitterDetailsComponent } from './sitter-details/sitter-details.component';
import { FormsModule } from '@angular/forms';

@NgModule({
  declarations: [
    AppComponent,
    RatingComponent,
    SittersListComponent,
    SitterDetailsComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
