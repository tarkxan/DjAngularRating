import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';

import { SitterService } from '../sitter.service';
import { Sitter } from '../sitter';

@Component({
  selector: 'app-sitters-list',
  templateUrl: './sitters-list.component.html',
  styleUrls: ['./sitters-list.component.css']
})
export class SittersListComponent implements OnInit {

  sitters: Observable<Sitter[]>;

  ratingClicked: number;
  rating: number = 1;

  constructor(private sitterService: SitterService) { }

  ngOnInit() {
    this.reloadData();
  }

  reloadData() {
    this.sitters = this.sitterService.getSittersByRating(this.rating);
  }

  sitterNameClicked = (sitter) => {
    this.sitterService.getSitter(sitter.id).subscribe(
      data => {
        console.log(data);
      },
      error => {
        console.log(error);
      }
    );
  }

  // return users rounded avd rating to print rating as stars
  arrayFilledStars(n: number): any[] {
    return Array(Math.round(n));
  }

  arrayEmptyStars(n: number): any[] {
    return Array(5 - Math.round(n));
  }

  // rating
  ratingComponentClick(clickObj: any): void {
    this.rating = clickObj.rating;
    this.ratingClicked = clickObj.rating;
    this.reloadData();
  }
}
