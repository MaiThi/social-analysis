import {Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import {TwitterResult} from '../../Model/twitterresult';
import {MatPaginator, MatSort, MatTableDataSource} from '@angular/material';
import {ProductServiceService} from '../../Service/ProductService.service';
import {NotificationService} from '../../Service/notification.service';

@Component({
  selector: 'app-twitter-dashboard',
  templateUrl: './twitter-dashboard.component.html',
  styleUrls: ['./twitter-dashboard.component.css']
})
export class TwitterDashboardComponent implements OnInit {
  displayedTwitterColumns: string[] = ['id', 'tweet', 'score'];
  twitterResult: TwitterResult[] = [];
  listTweetResult: MatTableDataSource<any>;
  averageTwitter: number;
  optionsTwitter: Object;
  mode = 'determinate';
  @ViewChild(MatPaginator) paginatorTwitter: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;
  constructor(private productService: ProductServiceService, private notificationService: NotificationService) { }

  ngOnInit() {
    this.productService.getTwitterResult().subscribe(
      resTwitter => {
        this.notificationService.success(':: Sentiment for news successfully');
        this.averageTwitter = resTwitter.averageTwitter;
        this.twitterResult = resTwitter.listTwitter;
        this.filterValueIntoMatSourceOfTwitter(this.twitterResult);
        this.optionsTwitter = {
            title : { text : 'Sentiment distribution for Twitter' },
            subtitle: {
                text: 'Source: '
            },
            chart: { type: 'column',
              width: 450,
              height: 300
            },
            xAxis: {
                categories: ['0-10', '10-20', '20-30', '30-40', '40-50'
                , '40-50', '50-60', '60-70', '70-80', '80-90', '90-100'],
                title: {
                    text: 'Sentiment Score %'
                }
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'Density',
                    align: 'high'
                },
                labels: {
                    overflow: 'justify'
                }
            },
             tooltip: {
                  valueSuffix: ' '
              },
             series: [{
                data: resTwitter.chartDataTwitter
            }]
        };
      },
      errorTwitter => {
         this.notificationService.warn(':: Error come from Twitter');
      }
      );
  }
   filterValueIntoMatSourceOfTwitter(twitterResult: TwitterResult[]) {
      this.listTweetResult = new MatTableDataSource(twitterResult);
      this.listTweetResult.paginator = this.paginatorTwitter;
      this.listTweetResult.filterPredicate =
        (data: TwitterResult, filter: string) => (data.id !== null) ? (data.score !== Number.parseFloat(filter)) : false;
    }

}
