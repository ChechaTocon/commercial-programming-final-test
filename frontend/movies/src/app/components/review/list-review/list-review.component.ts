import { Component, OnInit } from '@angular/core';
import { Subscription } from 'rxjs'
import { Apollo } from 'apollo-angular';
import gql from 'graphql-tag';
import { Review, User, Movie, CreateReview } from '../../../models/review.model'

const getReview = gql`
  query {
    reviews {
      id
      comment
      ranking
      createdAt
      updatedAt
      movie{
        id
        movieName
      }
      user{
        id
        username
      }
    }
  }
`;

@Component({
  selector: 'app-list-review',
  templateUrl: './list-review.component.html',
  styleUrls: ['./list-review.component.css']
})
export class ListReviewComponent implements OnInit {
  public cargando:boolean = false
  dataSource: Review[] | undefined
  private querySubscription: Subscription | undefined;

  constructor(private apollo: Apollo) { }

  ngOnInit(): void {
    this.querySubscription = this.apollo.watchQuery<any>({
      query: getReview
    })
      .valueChanges
      .subscribe(({ data }) => {
        this.dataSource = data.reviews;
        console.log(this.dataSource)        
      });
  }

  openDialog(id:number){
    console.log('myid:',id)
  }

}
