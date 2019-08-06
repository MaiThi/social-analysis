import {Context} from './context';
import {Sort} from './sort';
import {Item} from './item';

export class Search {
  type: string;
  readLink: string;
  queryContext: Context;
  totalEstimatedMatches: number;
  sort: Sort[];
  value: Item[];
}
