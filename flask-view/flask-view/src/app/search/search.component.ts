import { Component, OnInit } from '@angular/core';
import {ProductServiceService} from '../Service/ProductService.service';
import {Search} from '../Model/search';
import {Item} from '../Model/item';
import {Router} from '@angular/router';
import {NotificationService} from '../Service/notification.service';

@Component({
  selector: 'app-search',
  templateUrl: 'search.component.html',
  styleUrls: ['search.component.scss']
})
export class SearchComponent implements OnInit {

  search: Search;
  item: Item;
  keyword: string;
  private initialized = false;
  private username: string;
  private password: string;
  constructor(private productService: ProductServiceService,
              private route: Router,
              private notificationService: NotificationService) { }

  ngOnInit() {
    this.item = null;
    this.initialized = true;
    this.productService.deleteAllResults().subscribe(
       res => {},
       error1 => {}
     );
  }

  getItem() {
    this.notificationService.warn(':: Searching and Crawling infor');
    this.productService.getSearchsResult(this.keyword).subscribe(
      res => {
          this.notificationService.success(':: Search Engine successfully');
          this.item = res;
          this.route.navigate( ['/dashboard-result' ]);
      },
      error1 => {
          alert('Error come');
      }
    );
   /* this.productService.getSearchTwittersResult(this.keyword).subscribe(
      res => {
          this.route.navigate( ['/dashboard-result' ]);
      },
      error1 => {
        alert('Error come from twitter');
      }
    );*/
  }
}
