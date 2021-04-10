package slidingPuzzle;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;
import java.util.Vector;

import sac.graph.AStar;
import sac.graph.GraphSearchAlgorithm;
import sac.graph.GraphState;
import sac.graph.GraphStateImpl;

public class slidingPuzzle extends GraphStateImpl {
	
	public static final int n = 3;
	public static final int n2 = n * n;
	public static final int numberChangedBlock = 0;
	
	public byte[][] board;
	
	public static final String[] directions = {"L", "R", "D", "U"};
	
	public slidingPuzzle() {
		board = new byte[n][n];
		
		byte k = 0;
		for (int i = 0; i < n; i++) {
			for (int j = 0; j < n; j++, k++) {
				board[i][j] = k;
			}
		}
	}
	
	// konstruktor kopiujacy
	public slidingPuzzle(slidingPuzzle toCopy) {
		board = new byte[n][n];  // rezerwacja pamieci na tablice sudoku
		
		// wypelnienie tablicy sudoku wartosciami rodzica
		for (int i = 0; i < board.length; i++) {
			for (int j = 0; j < board.length; j++) {
				board[i][j] = toCopy.board[i][j];
			}
		}

	}
	
	@Override
	public String toString() {
		StringBuilder result = new StringBuilder();
		
		for (int i = 0; i < n; i++) {
			for (int j = 0; j < n; j++) {
				result.append(board[i][j]);
				result.append(",");
				
				if(j == n - 1) {
					result.append("\n");
				}
			}
		}
		
		return result.toString();
	}
	
	@Override
	public int hashCode() {  // funkcja mieszajaca
		return toString().hashCode();  // zmien najpierw na string i wtedy wylicz kod mieszajacy
	}
	
	public void mix(int counter) {
		Random r = new Random();
		
		for (int i = 0; i < counter; i++) {
			int random = Math.abs(r.nextInt() % (directions.length));
			int indexZero = findZero();
			String direction = directions[random];
			
			// czy wylosowany ruch nie jest poza granicami planszy
			if(!moveIsLegal(indexZero, direction)) {
				i--;  // aby na pewno wykonala sie zadana liczba przestawien
				continue;  // losuj dalej
			}
			
			int calculationPosition = indexZero + moveWhere(direction);  // indeks, gdzie jest zero + przesuniecie w odpowiednim kierunku
			swap(indexZero, calculationPosition);  // zamien klocek z sasiadem
			
		}
		
		// przykladowa ukladanka - poniewaz nie kazda jest rozwiazywalna
//		board[0][0] = 3;
//		board[0][1] = 7;
//		board[0][2] = 4;
//		board[1][0] = 0;
//		board[1][1] = 5;
//		board[1][2] = 6;
//		board[2][0] = 8;
//		board[2][1] = 2;
//		board[2][2] = 1;
	}
	
	private int getInvCount(byte[][] arr) 
	{ 
	    int inv_count = 0; 
	    for (int i = 0; i < n - 1; i++) {
	        for (int j = i + 1; j < n; j++)  {
	          
	            // Value 0 is used for empty space 
	            if (arr[j][i] > 0 && arr[j][i] > arr[i][j]) {
	                inv_count++; 
	            }
	        }
	    }
	    
	    return inv_count; 
	} 
	  
	public boolean isSolvable() 
	{ 
	    int invCount = getInvCount(board); 
	  
	    return (invCount % 2 == 0); 
	} 
	
	public boolean moveIsLegal(int position, String direction) {  // sprawdza, czy wybrany klocek i kierunek nie koliduja z granicami planszy
		int i = position / n, j = position % n;
		
		if (i == (n - 1)) {  // dolny wiersz
			if (direction == "D") {
				return false;
			}
			else if (j == 0 && direction == "L") {  // lewy dolny rog
				return false;
			}
			else if (j == (n-1) && direction == "R") {  // prawy dolny rog
				return false;
			}
		}
		else if (i == 0) {  // gorny wiersz
			if (direction == "U") {
				return false;
			}
			else if (j == 0 && direction == "L") {  // lewy gorny rog
				return false;
			}
			else if (j == (n - 1) && direction == "R") {  // prawy gorny rog
				return false;
				
			}
		}
		else {  
			if (j == 0 && direction == "L") {  // komorki po lewej stronie (lewa kolumna)
				return false;
			}
			else if(j == (n - 1) && direction == "R") {  // komorki po prawej stronie (prawa kolumna)
				return false;
			}
		}
		
		return true;
	}
	
	private boolean isLegal_block(int block) {
		for (int i = 0, k = 0; i < board.length; i++) {
			for (int j = 0; j < board.length; j++, k++) {
				if (k == block && k == board[i][j]) {  // czy bloczek ze swoim numerem jest na odpowiedniej pozycji
					return true;
				}
			}
		}
		
		return false;
	}
	
	public int moveWhere(String direction) {
		if(direction == "L") {
			return -1;
		}
		else if (direction == "R") {
			return 1;
		}
		else if (direction == "U") {
			return -n;
		}
		else {
			return n;
		}
	}
	
	public void swap(int position1, int position2) {
		int i1 = position1 / n, j1 = position1 % n;
		int i2 = position2 / n, j2 = position2 % n;
		
		byte b1 = board[i1][j1];
		byte b2 = board[i2][j2];
		
		board[i1][j1] = b2;
		board[i2][j2] = b1;
	}
	
	public int findZero() {
		int k = 0;
		
		setK:
		for (int i = 0; i < board.length; i++) {
			for (int j = 0; j < board.length; j++, k++) {
				if(board[i][j] == 0) {
					break setK;
				}
			}
		}
		
		return k;
	}
	
	@Override
	public List<GraphState> generateChildren() {
		List<GraphState> children = new ArrayList<GraphState>();
		
		// wyszukanie gdzie jest klocek 0 i zbadanie, czy otaczajacy go koledzy sa na swoim miejscu
		for (String direction : directions) {
			int zeroIndex = findZero();
			
			// sprawdzenie, czy w wybranym kierunku mozna zamienic klocek
			if(moveIsLegal(zeroIndex, direction)) {
				// sprawdzenie, czy klocek wybrany do zamiany jest na swoim miejscu
				int calculationPosition = zeroIndex + moveWhere(direction);  // indeks, gdzie jest zero + przesuniecie w odpowiednim kierunku
				
				//if (!isLegal_block(calculationPosition)) {  
					slidingPuzzle child = new slidingPuzzle(this);  // kopia tego obiektu
					
//					System.out.println("--------");
//					System.out.println("stan poczatkowy ukladanki:\n" + child);
					
					child.swap(zeroIndex, calculationPosition);  // zamien klocek co jest nie na swoim miejscu z sasiadem
					child.setMoveName(direction);  // zapisanie, w ktora strone ten klocek zostal przesuniety
					
					children.add(child);  // zapisz to rozgalezienie
					
//					System.out.println("0 jest na indeksie " + zeroIndex + ". przesunieto 0 " + " w kierunku " + direction + " z klockiem o indeksie " + calculationPosition + " wartosc(" + 
//					board[(int) (calculationPosition/n)][(calculationPosition%n)] + ") na indeks " + zeroIndex);
//					System.out.println("stan koncowy ukladanki:\n" + child);
				//}
			}
		}
		
		return children;
	}

	@Override
	public boolean isSolution() {
		byte k = 0;
		for (int i = 0; i < n; i++) {
			for (int j = 0; j < n; j++, k++) {
				if (k != board[i][j]) {
					return false;
				}
			}
		}
		return true;
	}
	
	public static void main(String[] args) {
		
		
//		System.out.println(p);
//		System.out.println("Czy obecne ulozenie jest rozwiazaniem? Odp.: " + p.isSolution());
//		System.out.println("Czy ukladanka jest rozwiazywalna? Odp.: " + p.isSolvable());
		
		int problems = 1;
		
		long[] times1 = new long[problems];
		int[] closed_states1 = new int[problems];
		int[] open_states1 = new int[problems];
		int[] path_long1 = new int[problems];
		
		long[] times2 = new long[problems];
		int[] closed_states2 = new int[problems];
		int[] open_states2 = new int[problems];
		int[] path_long2 = new int[problems];
		
		for (int i = 0; i < problems; i++) {
			slidingPuzzle p = new slidingPuzzle();
			p.mix(1000);
			
			// heurystyka MisplacedTiles
			slidingPuzzle.setHFunction(new MisplacedTilesHeuristic());
			GraphSearchAlgorithm a1 = new AStar(p);
			a1.execute();
			
			GraphState sol1 = a1.getSolutions().get(0);
			List<GraphState> paths1 = sol1.getPath();
//			for (GraphState path : paths1) {
//				System.out.println("---");
//				System.out.println(path);
//			}
			
			List<String> steps1 = sol1.getMovesAlongPath();
			for (String step : steps1) {
				System.out.print(step + ",");
			}
			System.out.print("\n");
			
//			System.out.println("Time [ms]: " + a1.getDurationTime());
//			System.out.println("Closed: " + a1.getClosedStatesCount());
//			System.out.println("Open: " + a1.getOpenSet().size());  // liczba oznaczajaca ilosc stanow, ktorymi algorytm mogl isc, ale sie zatrzymal, bo napotkal isSolution()
//			System.out.println("Solutions: " + a1.getSolutions().size());
			
			times1[i] = a1.getDurationTime();
			closed_states1[i] = a1.getClosedStatesCount();
			open_states1[i] = a1.getOpenSet().size();
			path_long1[i] = sol1.getPath().size();
			
			// heurystyka Manhattan
			slidingPuzzle.setHFunction(new ManhattanHeuristic());
			GraphSearchAlgorithm a2 = new AStar(p);
			a2.execute();
			
			GraphState sol2 = a2.getSolutions().get(0);
			List<GraphState> paths2 = sol2.getPath();
//			for (GraphState path : paths2) {
//				System.out.println("---");
//				System.out.println(path);
//			}
			
			List<String> steps2 = sol2.getMovesAlongPath();
			for (String step : steps2) {
				System.out.print(step + ",");
			}
			System.out.print("\n");
			
//			System.out.println("Time [ms]: " + a2.getDurationTime());
//			System.out.println("Closed: " + a2.getClosedStatesCount());
//			System.out.println("Open: " + a2.getOpenSet().size());  // liczba oznaczajaca ilosc stanow, ktorymi algorytm mogl isc, ale sie zatrzymal, bo napotkal isSolution()
//			System.out.println("Solutions: " + a2.getSolutions().size());
			
			times2[i] = a2.getDurationTime();
			closed_states2[i] = a2.getClosedStatesCount();
			open_states2[i] = a2.getOpenSet().size();
			path_long2[i] = sol2.getPath().size();
		}
		
		System.out.println("---------- Misplaced tiles ----------");
		System.out.println("Sredni czas [ms]: " + (Arrays.stream(times1).sum() / problems));
		System.out.println("Laczny czas [ms]: " + Arrays.stream(times1).sum());
		System.out.println("Srednia ilosc stanow zamknietych: " + (Arrays.stream(closed_states1).sum() / problems));
		System.out.println("Srednia ilosc stanow otwartych: " + (Arrays.stream(open_states1).sum() / problems));
		System.out.println("Srednia dlugosc sciezki: " + (Arrays.stream(path_long1).sum() / problems));
		System.out.print("\n");
		
		System.out.println("---------- Manhattan ----------");
		System.out.println("Sredni czas [ms]: " + (Arrays.stream(times2).sum() / problems));
		System.out.println("Laczny czas [ms]: " + Arrays.stream(times2).sum());
		System.out.println("Srednia ilosc stanow zamknietych: " + (Arrays.stream(closed_states2).sum() / problems));
		System.out.println("Srednia ilosc stanow otwartych: " + (Arrays.stream(open_states2).sum() / problems));
		System.out.println("Srednia dlugosc sciezki: " + (Arrays.stream(path_long2).sum() / problems));
	
	}
	
}
