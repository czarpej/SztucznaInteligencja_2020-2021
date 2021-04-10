package Connect4;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Scanner;

import sac.game.AlphaBetaPruning;
import sac.game.GameSearchAlgorithm;
import sac.game.GameState;
import sac.game.GameStateImpl;

public class Connect4 extends GameStateImpl {
	
	public static final int m = 8;
	public static final int n = 8;
	
	
	public static enum states {
		X,  // gracz maksymalizujacy
		O,  // gracz minimalizujacy
		$  // puste stany
	}
	
	public states[][] board;
	
	Connect4(boolean whoMove) {
		board = new states[m][n];
		
		for (int i = 0; i < m; i++) {
			for (int j = 0; j < n; j++) {
				board[i][j] = states.$;
			}
		}
		
		setMaximizingTurnNow(whoMove);  // ustawienie flagi ruchu
	}
	
	Connect4(Connect4 toCopy) {
		board = new states[m][n];  // rezerwacja pamieci na tablice sudoku
		
		// wypelnienie tablicy sudoku wartosciami rodzica
		for (int i = 0; i < m; i++) {
			for (int j = 0; j < n; j++) {
				board[i][j] = toCopy.board[i][j];
			}
		}
		
		setMaximizingTurnNow(toCopy.isMaximizingTurnNow());  // zmiana flagi ruchu w stosunku do rodzica
	}
	
	@Override
	public int hashCode() {  // funkcja mieszajaca
		return toString().hashCode();  // zmien najpierw na string i wtedy wylicz kod mieszajacy
	}
	
	@Override
	public String toString() {
		StringBuilder result = new StringBuilder();
		
		for (int i = 0; i < m; i++) {
			for (int j = 0; j < n; j++) {
				result.append((board[i][j] == states.$) ? "." : board[i][j]);
				result.append("  ");
				
				if(j == n - 1) {
					result.append("\n");
				}
			}
		}
		
		for (int i = 0; i < n; i++) {
			result.append(i);
			result.append("  ");
		}
		result.append("\n");
		
		return result.toString();
	}
	
	public void pushSign(int i, int j) {
		if(isMaximizingTurnNow()) {
			board[i][j] = states.X;
		}
		else {
			board[i][j] = states.O;
		}
	}
	
	public void move(int column) {
		// znajdowanie ktora kolumna
		for (int i = 0; i < m - 1; i++) {
			if(board[i + 1][column] != states.$) {  // jak w nastepnej kolumnie jest juz cos wrzucone
				pushSign(i, column);  // to wrzuc do obecnej odpowiedni znaczek
				break;  // dalej juz nie nie wpisuj	
			}
			else if(i == (m - 1 - 1) && board[i + 1][column] == states.$) {  // dol mapy
				pushSign(i + 1, column);
			}
		}
		
		// zmiana flagi ruchu
		setMaximizingTurnNow(!isMaximizingTurnNow());
	}

	@Override
	public List<GameState> generateChildren() {
		List<GameState> children = new ArrayList<GameState>();

		for (int i = 0; i < n; i++) {
			Connect4 child = new Connect4(this);
			child.move(i);
			child.setMoveName("" + i);
			children.add(child);
		}
		
		return children;
	}
	
	public static void main(String[] args) {
		boolean maxPlayer = false;  // czy pierwszy rusza gracz maksymalizujacy
		boolean humanPlayer = true;  // czy gra czlowiek-komputer
		
		Connect4 c4 = new Connect4(maxPlayer);
		Connect4.setHFunction(new PositionHeuristic());
		
		System.out.println("\n----------- Aktualny stan planszy: -----------");
		System.out.println(c4);
		
		// testowanie naprzemiennych ruchow
//		while(true) {
//			Scanner scan = new Scanner(System.in);
//			System.out.println("W ktora kolumne wrzucic?");
//			int column;
//			do {
//				column = scan.nextInt();
//			} while(column < 0 || column > c4.m);
//			c4.move(column);
//			System.out.println("Stan planszy po wykonaniu ruchu:");
//			System.out.println(c4);
//		}
		
		GameSearchAlgorithm algo = new AlphaBetaPruning(c4);
		Scanner scan = new Scanner(System.in);
		boolean victory = false;
		
		while(!victory) {
			
			// sprawdzenie czy tura gracza
			if(c4.isMaximizingTurnNow() && humanPlayer) {
				System.out.println("Ruch gracza");
				
				System.out.println("W ktora kolumne wrzucic?");
				int column;
				do {
					column = scan.nextInt();
				} while(column < 0 || column > Connect4.n);
				
				c4.move(column);
			}
			else {
				// obliczenie szans
				algo.setInitial(c4);
				algo.execute();
				Map<String, Double> movesScores = algo.getMovesScores();
				String best = algo.getFirstBestMove();
				
				System.out.println("Ruch komputera...");
				System.out.println("Oceny ruchow:");
				for (Map.Entry<String, Double> movesEntry : movesScores.entrySet()) {
				    final String column = movesEntry.getKey();
				    final Double heuristicValue = movesEntry.getValue();
				    System.out.println("Kolumna: " + column + ", Ocena: " + heuristicValue);
				}
//				for( int i = 0; i < Connect4.n; i++ ) {
//					System.out.println("Kolumna: " + i + ", Ocena: " + movesScores.get("" + i));
//				}
				System.out.println("Komputer wrzuca w kolumne " + best);
				c4.move(Integer.valueOf(best));
				
			}
			
			System.out.println("\n----------- Aktualny stan planszy: -----------");
			System.out.println(c4);
			
			// sprawdzenie warunkow zwyciestwa
			Guardian g = new Guardian();
			series4Seeker:
			for (int i = 0; i < Connect4.m; i++) {
				for (int j = 0; j < Connect4.n; j++) {
					// dotkniecie sufitu
					if(i == 0) {
						if(c4.board[i][j] != Connect4.states.$) {
							victory = true;
							break series4Seeker;
						}
					}
					
					// ciag o dlugosci 4
					if(Double.isInfinite(g.focus(c4, i, j))) {
						victory = true;
						break series4Seeker;
					}
				}
			}
		}
		
		scan.close();
		
		if(c4.isMaximizingTurnNow()) { 
			System.out.println("Wygral komputer");
		}
		else {
			System.out.println("Wygral czlowiek");
		}
	}

	
}
