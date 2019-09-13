import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {Observable} from 'rxjs';
import {Product} from '../Model/Product';
import {Item} from '../Model/item';
import {ResponseDashboardNew} from '../Model/response';
import {ResponseDashboardTwitter} from '../Model/responseTwitter';

@Injectable({
  providedIn: 'root'
})
export class ProductServiceService {

  private BASE_URL = 'http://localhost:5000/';
  private PRODUCT_URL = this.BASE_URL + 'products';
  private SAVE_UPDATE_LOCATION_URL = this.PRODUCT_URL;
  private SEARCH_URL = this.BASE_URL + 'search';
  private TWITTER_SEARCH_URL = this.BASE_URL + 'twitterAnalysis';
  constructor(private http: HttpClient) { }

  getProducts(): Observable<Product[]> {
    return this.http.get<Product[]>(this.PRODUCT_URL);
  }

  getProductById(id: number): Observable<Product> {
    return this.http.get<Product>(this.PRODUCT_URL + '/' + id);
  }

  getSearchsResult(keyword: string): Observable<Item> {
    return this.http.get<Item>(this.SEARCH_URL + '/' + keyword);
  }
  getDashboardResult(): Observable<ResponseDashboardNew> {
    return this.http.get<ResponseDashboardNew>(this.BASE_URL + 'analysic', { headers: new HttpHeaders({ timeout: `${200000}` }) });
  }
  getSearchTwittersResult(keyword: string): Observable<string> {
    return this.http.get<string>(this.TWITTER_SEARCH_URL + '/' + keyword);
  }
  getTwitterResult(): Observable<ResponseDashboardTwitter> {
    return this.http.get<ResponseDashboardTwitter>(this.BASE_URL + 'get-twitters');
  }
  deleteAllResults(): Observable<any> {
    return this.http.get<any>(this.BASE_URL + 'searched/deleteAll');
  }
}
