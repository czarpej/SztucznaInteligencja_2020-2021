package sudoku;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import sac.graph.BestFirstSearch;
import sac.graph.GraphSearchAlgorithm;
import sac.graph.GraphSearchConfigurator;
import sac.graph.GraphState;
import sac.graph.GraphStateImpl;

public class Sudoku extends GraphStateImpl {
	
	public static final int n = 3;
	public static final int n2 = n * n;
	
	// typy zmiennych w Java:
	// byte - 1bit ze znakiem, short - 2bit, int - 4bit, long - 8bit
	// float - 4bit, float - 8bit (IEEE 754)
	// boolean - 1bit, char - 2bit (ascii)
	
	public byte[][] board;
	private int zeros = n2 * n2;
	
	public Sudoku() {
		board = new byte[n2][n2];  // rezerwacja pamieci na tablice sudoku
		
		// wypelnienie tablicy sudoku zerami
		for (int i = 0; i < board.length; i++) {
			for (int j = 0; j < board.length; j++) {
				board[i][j] = 0;
			}
		}
	}
	
	// konstruktor kopiujacy
	public Sudoku(Sudoku toCopy) {
		board = new byte[n2][n2];  // rezerwacja pamieci na tablice sudoku
		
		// wypelnienie tablicy sudoku wartosciami rodzica
		for (int i = 0; i < board.length; i++) {
			for (int j = 0; j < board.length; j++) {
				board[i][j] = toCopy.board[i][j];
			}
		}
		
		zeros = toCopy.zeros;  // ile jest zer, informacja z rodzica
	}
	
	public int getZeros() {
		return zeros;
	}

	@Override
	public String toString() {
//		String result = "";
		// 0, 1, 0, ..., 9 \n
		
//		for (int i = 0; i < n2; i++) {
//			for (int j = 0; j < n2; j++) {
//				result += board[i][j] + ",";
				
//				if(j == n2 - 1) {
//					result += "\n";
//				}
//			}
//		}
		
//		return result;
		
		StringBuilder result = new StringBuilder();
		
		for (int i = 0; i < n2; i++) {
			for (int j = 0; j < n2; j++) {
				result.append(board[i][j]);
				result.append(",");
				
				if(j == n2 - 1) {
					result.append("\n");
				}
			}
		}
		
		return result.toString();
	}

	@Override
	public int hashCode() {  // funkcja mieszajaca
		// return toString().hashCode();  // zmien najpierw na string i wtedy wylicz kod mieszajacy
		
		// szybszy sposob
		byte[] linear = new byte[n2 * n2];  // liniowa tablica przechowujaca sudoku
		int k = 0;
		
		for (int i = 0; i < n2; i++) {
			for (int j = 0; j < n2; j++) {
				linear[k++] = board[i][j];
			}
		}
		
		return Arrays.hashCode(linear);
	}

	public void fromStringN3(String txt) {
		int k = 0;
		for (int i = 0; i < n2; i++) {
			for (int j = 0; j < n2; j++) {
				board[i][j] = Byte.valueOf(txt.substring(k, k + 1));
				k++;
			}
		}
		
		refreshZeros();  // po kazdym wypisaniu planszy zlicza ile jest zer w planszy
	}
	
	public boolean isLegal() {
		byte[] group = new byte[n2];  // wspoldzielona tablica bajtow
		
		// rows
		for (int i = 0; i < group.length; i++) {
			// wewnetrzna petla jedynie na zrobienie kopii wiersza
			for (int j = 0; j < group.length; j++) {
				group[j] = board[i][j];
			}
			
			// po zrobieniu kopii wiersza sprawdzenie czy grupa jest legalna
			if(!isGroupLegal(group))
				return false;
		}
		
		// columns
		for (int i = 0; i < group.length; i++) {
			// wewnetrzna petla jedynie na zrobienie kopii wiersza
			for (int j = 0; j < group.length; j++) {
				group[j] = board[j][i];
			}
			
			// po zrobieniu kopii wiersza sprawdzenie czy grupa jest legalna
			if(!isGroupLegal(group))
				return false;
		}
		
		// squares - petle skaczace po kwadratach
		for(int i = 0; i < n; i++) {
			for(int j = 0; j < n; j++) {
				int q = 0;
				
				// petle odpowiedzialne za kopiowanie kwadratow
				for(int k = 0; k < n; k++) {
					for(int l = 0; l < n; l++) {
						group[q++] = board[i * n + k][j * n + l];
					}
				}
				
				if(!isGroupLegal(group))
					return false;
			}
		}
		
		return true;
	}
	
	private boolean isGroupLegal(byte[] group) {
		boolean[] visited = new boolean[n2];  // tablica odwiedzin
		
		// wypelnienie wstepnymi wartosciami
		for (int i = 0; i < visited.length; i++) {
			visited[i] = false;
		}
		
		for (int i = 0; i < visited.length; i++) {
			if(group[i] == 0)
				continue;
			
			if(visited[group[i] - 1])
				return false;
			
			visited[group[i] - 1] = true;
		}
		
		return true;
	}
	
	private void refreshZeros() {
		// zlicza ile jest zer w planszy sudoku
		zeros = 0;
		for (int i = 0; i < n2; i++) {
			for (int j = 0; j < n2; j++) {
				if(board[i][j] == 0)
					zeros++;
			}
		}
	}
	
	@Override
	public List<GraphState> generateChildren() {
		List<GraphState> children = new ArrayList<GraphState>();
		
		int i = 0, j = 0;
		
		zeroSeeker:
		for (i = 0; i < n2; i++) {
			for (j = 0; j < n2; j++) {
				if(board[i][j] == 0)
					break zeroSeeker;  // przerwie petle o nazwie zeroSeeker
			}
		}
		
		if (i == n2)  // ten break zeroSeeker nie zaistnial
			return children;
		
		// generowanie stanow potomnych
		for (int k = 0; k < n2; k++) {
			Sudoku child = new Sudoku(this);  // kopia tego obiektu
			child.board[i][j] = (byte) (k + 1);  // operacja dodawania zawsze zostawia wynik w int w jezyku Java, a tablica board jest typu byte
			
			if(child.isLegal()) {
				children.add(child);
				child.zeros--;
			}
		}
		
		return children;
	}
	
	@Override
	public boolean isSolution() {  // sprawdza czy ustawienie sudoku jest rozwiazaniem
		return ((zeros == 0) && (isLegal()));
	}

	public static void main(String[] args) {
		// String sudokuAsString = "003020600900305001001806400008102900700000008006708200002609500800203009005010300";
		String sudokuAsString = "000000000000305001001806400008102900700000008006708200002609500800203009005010300";
		
		Sudoku s = new Sudoku();
		s.fromStringN3(sudokuAsString);
		System.out.println(s);
		System.out.println(s.zeros);
		
		Sudoku.setHFunction(new EmptyCellsHeuristics());
		GraphSearchConfigurator conf = new GraphSearchConfigurator();
		conf.setWantedNumberOfSolutions(Integer.MAX_VALUE);  // liczba wymaganych przez nas rozwiazan (domyslnie jest 1)
		GraphSearchAlgorithm algo = new BestFirstSearch(s, conf);
		algo.execute();
		algo.getSolutions();
		List<GraphState> solutions = algo.getSolutions();
		for (GraphState sol : solutions) {
			System.out.println("---");
			System.out.println(sol);
		}
		
		System.out.println("Time [ms]: " + algo.getDurationTime());
		System.out.println("Closed: " + algo.getClosedStatesCount());
		System.out.println("Open: " + algo.getOpenSet().size());  // liczba oznaczajaca ilosc stanow, ktorymi algorytm mogl isc, ale sie zatrzymal, bo napotkal isSolution()
		System.out.println("Solutions: " + algo.getSolutions().size());
	}
	
	public static void main2(String[] args) {
		Object o1 = new Object();
		Object o2 = new Object();
		Object o3 = o1;  // takie same
		System.out.println(o1.hashCode());
		System.out.println(o2.hashCode());
		System.out.println(o3.hashCode());
	}
	
	public static void main3(String[] args) {
		Object o1 = new String("abc");
		Object o2 = new String("abc");
		// takie same
		System.out.println(o1.hashCode());
		System.out.println(o2.hashCode());
	}
	
	public static void main4(String[] args) {
		int[] o1 = new int[] {7, 1, 13};
		int[] o2 = new int[] {7, 1, 13};
		// normalnie inne, dzieki Arrays kody sa takie same
		System.out.println(Arrays.hashCode(o1));
		System.out.println(Arrays.hashCode(o2));
	}
	
}
