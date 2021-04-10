package slidingPuzzle;

import sac.State;
import sac.StateFunction;

public class MisplacedTilesHeuristic extends StateFunction {
	@Override
	public double calculate(State state) {
		slidingPuzzle p = (slidingPuzzle) state;

		byte k = 0, h = 0;
		
		for (int i = 0; i < p.board.length; i++) {
			for (int j = 0; j < p.board.length; j++, k++) {
				if (p.board[i][j] == 0) {
					continue;
				}
				
				if (p.board[i][j] != k) {
					h++;
				}
			}
		}
		
		return h;
	}
}
