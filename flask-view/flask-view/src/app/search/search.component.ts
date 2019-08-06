import { Component, OnInit } from '@angular/core';
import {ProductServiceService} from '../Service/ProductService.service';
import {Search} from '../Model/search';
import {Item} from '../Model/item';
import {Router} from '@angular/router';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss']
})
export class SearchComponent implements OnInit {

  search: Search;
  item: Item;
  keyword: string;
  constructor(private productService: ProductServiceService,
              private route: Router) { }

  ngOnInit() {
    this.item = null;
    this.productService.deleteAllResults().subscribe(
      res => {},
      error1 => {}
    );
  }
  test() {
    alert('abc');
  }
  getItem() {
    this.productService.getSearchsResult(this.keyword).subscribe(
      res => {
          this.item = res;
          this.route.navigate( ['/dashboard-result' ]);
      },
      error1 => {
          alert('Error come');
      }
    );
  }
}
