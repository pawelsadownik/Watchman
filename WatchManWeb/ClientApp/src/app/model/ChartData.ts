export class ChartData {
    category: string;
    red: number;
    yellow: number;

    constructor(data: {
    category: string,
    red: number,
    yellow: number
  }) {
    Object.assign(this, data);
  }
}
