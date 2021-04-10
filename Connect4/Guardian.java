package Connect4;

import Connect4.Connect4.states;

public class Guardian {
	// klasa wewnetrzna sluzaca jako para do zliczania wartosci wystapien stanow X, O
	public final class Series {
		public int X, O;
		
		Series() {
			X = 0;
			O = 0;
		}
		
		public void add(Series s) {
			this.X += s.X;
			this.O += s.O;
		}
		
	}
	
	// ile pozycji moze sprawdzic patrzac w gore
	private int posDist_top(Connect4 c4, int i, int j) {
		int h = 0;
		
		if(i < 3) {  // jak jest 0, 1, 2, 3 to odpowiednio tyle pozycji moze sprawdzic
			h = i % 3;
		}
		else {
			h = 3;  // moze sprawdzic zawsze 3 pozycje do przodu
		}
		
		return h;
	}
	
	// ile pozycji moze sprawdzic patrzac w dol
	private int posDist_bottom(Connect4 c4, int i, int j) {
		int h = 0;
		
		if ((Connect4.m - 1 - i) < 3) {
			h = Connect4.m - 1 - i;
		}
//		if(i > 2) {  // jak jest 3, 4, 5 to odwrotnie proporcjonalnie pozycji moze sprawdzic
//			h = Connect4.m - 1 - i;
//		}
		else { 
			h = 3;  // moze sprawdzic zawsze 3 pozycje do przodu
		}
		
		return h;
	}
	
	// ile pozycji moze sprawdzic patrzac w lewo
	private int posDist_left(Connect4 c4, int i, int j) {
		int h = 0;
		
		if(j < 4) {
			h = j % 4;  // jak jest 0, 1, 2, 3 to odpowiednio tyle pozycji moze sprawdzic
		}
		else {
			h = 3;  // moze sprawdzic zawsze 3 pozycje do przodu
		}
		
		return h;
	}
	
	// ile pozycji moze sprawdzic patrzac w prawo
	private int posDist_right(Connect4 c4, int i, int j) {
		int h = 0;
		
		if((Connect4.n - 1 - j) < 3) {
			h = Connect4.n - 1 - j;
		}
//		if(j > 3) {
//			h = Connect4.n - 1 - j;  // jak jest 4, 5, 6 to odwrotnie proporcjonalnie pozycji moze sprawdzic
//		}
		else {
			h = 3;  // moze sprawdzic zawsze 3 pozycje do przodu
		}
		
		return h;
	}
	
	// ile pozycji moze sprawdzic patrzac po skosie gora-lewo
	private int posDist_topLeft(Connect4 c4, int i, int j) {
		int h = 0;
		
		int top = posDist_top(c4, i, j);  // ile pozycji moze sprawdzic w gore
		int left = posDist_left(c4, i, j);  // ile pozycji moze sprawdzi w lewo
		h = Math.min(top, left);  // w wyniku kompromisu sprawdzania po skosie wybiera najmniejsza wartosc
		
		return h;
	}
	
	// ile pozycji moze sprawdzic patrzac po skosie gora-prawo
	private int posDist_topRight(Connect4 c4, int i, int j) {
		int h = 0;
		
		int top = posDist_top(c4, i, j);  // ile pozycji moze sprawdzic w gore
		int right = posDist_right(c4, i, j);  // ile pozycji moze sprawdzi w prawo
		h = Math.min(top, right);  // w wyniku kompromisu sprawdzania po skosie wybiera najmniejsza wartosc
		
		return h;
	}
	
	// ile pozycji moze sprawdzic patrzac po skosie gora-prawo
	private int posDist_bottomLeft(Connect4 c4, int i, int j) {
		int h = 0;
		
		int bottom = posDist_bottom(c4, i, j);  // ile pozycji moze sprawdzic w dol
		int left = posDist_left(c4, i, j);  // ile pozycji moze sprawdzi w lewo
		h = Math.min(bottom, left);  // w wyniku kompromisu sprawdzania po skosie wybiera najmniejsza wartosc
		
		return h;
	}
	
	// ile pozycji moze sprawdzic patrzac po skosie gora-prawo
	private int posDist_bottomRight(Connect4 c4, int i, int j) {
		int h = 0;
		
		int bottom = posDist_bottom(c4, i, j);  // ile pozycji moze sprawdzic w dol
		int right = posDist_right(c4, i, j);  // ile pozycji moze sprawdzi w prawo
		h = Math.min(bottom, right);  // w wyniku kompromisu sprawdzania po skosie wybiera najmniejsza wartosc
		
		return h;
	}
	
	// zlicza w wystapienia X oraz O
	private Series countSeries(Connect4 c4, int i, int j) {
		Series series = new Series();
		
		if(c4.board[i][j] == Connect4.states.X) {
			series.X++;
		}
		else if(c4.board[i][j] == Connect4.states.O) {
			series.O--;
		}
		
		return series;
	}
	
	// oblicza czego jest wiecej
	private double calculateH(Series s) {
		double h = 0;
		
		if(s.X == 4 && s.O == 0) {
			// System.out.println("X jest 4");
			h = Double.POSITIVE_INFINITY;
		}
		else if(s.O == -4 && s.X == 0) {
			// System.out.println("O jest 4");
			h = Double.NEGATIVE_INFINITY;
		}
//		else if(s.X == 3 && s.O == 0) {
//			h = s.X + 20;
//		}
//		else if(s.O == -3 && s.X == 0) {
//			h = s.O - 20;
//		}
		else if(s.X > 1 && s.O == 0) {  // nie ma zadnych O
			h = s.X;  // + do oceny
		}
		else if(s.O < -1 && s.X == 0) {  // nie ma zadnych X
			h = s.O;  // - do oceny, poniewaz O < 0
		}
		
		return h;
	}
	
	public double focus(Connect4 c4, int i, int j) {
		double h = 0;  // ocena
		
		// regula sufitu
		if(i == 0) {
			if(c4.board[i][j] == states.X) {
				h = Double.POSITIVE_INFINITY;
			}
			else if(c4.board[i][j] == states.O) {
				h = Double.NEGATIVE_INFINITY;
			}
		}
		
		// sprawdzenie w kolumnie do gory
		if(posDist_top(c4, i, j) == 3) {
			Series series = new Series();
			for (int k = i; k >= i - posDist_top(c4, i, j); k--) {
				series.add(countSeries(c4, k, j));
			}
			
			double localH = calculateH(series);
			h += localH;
			
			if(Double.isInfinite(h)) {
				return h;
			}
		}
		
		// sprawdzenie w kolumnie do dolu
		if(posDist_bottom(c4, i, j) == 3) {
			Series series = new Series();
			for (int k = i; k <= i + posDist_bottom(c4, i, j); k++) {
				series.add(countSeries(c4, k, j));
			}
			
			double localH = calculateH(series);
			h += localH;
			
			if(Double.isInfinite(h)) {
				return h;
			}
		}
		
		// sprawdzenie w wierszu w lewo
		if(posDist_left(c4, i, j) == 3) {
			Series series = new Series();
			for (int k = j; k >= j - posDist_left(c4, i, j); k--) {
				series.add(countSeries(c4, i, k));
			}
			
			double localH = calculateH(series);
			h += localH;
			
			if(Double.isInfinite(h)) {
				return h;
			}
		}
		
		// sprawdzenie w wierszu w prawo
		if(posDist_right(c4, i, j) == 3) {
			Series series = new Series();
			for (int k = j; k <= j + posDist_right(c4, i, j); k++) {
				series.add(countSeries(c4, i, k));		
			}
			
			double localH = calculateH(series);
			h += localH;
			
			if(Double.isInfinite(h)) {
				return h;
			}
		}
		
		// sprawdzenie po skosie gora-lewo
		if(posDist_topLeft(c4, i, j) == 3) {
			Series series = new Series();
			for (int k = i, l = j; k >= i - posDist_top(c4, i, j) && l >= j - posDist_left(c4, i, j); k--, l--) {
				series.add(countSeries(c4, k, l));
			}
			
			double localH = calculateH(series);
			h += localH;
			
			if(Double.isInfinite(h)) {
				return h;
			}
		}
		
		// sprawdzenie po skosie gora-prawo
		if(posDist_topRight(c4, i, j) == 3) {
			Series series = new Series();
			for (int k = i, l = j; k >= i - posDist_top(c4, i, j) && l <= j + posDist_right(c4, i, j); k--, l++) {
				series.add(countSeries(c4, k, l));
			}
			
			double localH = calculateH(series);
			h += localH;
			
			if(Double.isInfinite(h)) {
				return h;
			}
		}
		
		// sprawdzenie po skosie dol-lewo
		if(posDist_bottomLeft(c4, i, j) == 3) {
			Series series = new Series();
			for (int k = i, l = j; k <= i + posDist_bottom(c4, i, j) && l >= j - posDist_left(c4, i, j); k++, l--) {
				series.add(countSeries(c4, k, l));
			}
			
			double localH = calculateH(series);
			h += localH;
			
			if(Double.isInfinite(h)) {
				return h;
			}
		}
		
		// sprawdzenie po skosie dol-prawo
		if(posDist_bottomRight(c4, i, j) == 3) {
			Series series = new Series();
			for (int k = i, l = j; k <= i + posDist_bottom(c4, i, j) && l <= j + posDist_right(c4, i, j); k++, l++) {
				series.add(countSeries(c4, k, l));
			}
			
			double localH = calculateH(series);
			h += localH;
			
			if(Double.isInfinite(h)) {
				return h;
			}
		}
		
		return h;
	}
}
