package Connect4;

import sac.State;
import sac.StateFunction;

public class PositionHeuristic extends StateFunction {
	@Override
	public double calculate(State state) {
		Connect4 c4 = (Connect4) state;

		Guardian g = new Guardian();
		double h = 0;  // ocena
		
		// sprawdzanie skupien na obrebie 4 pol
		for (int i = 0; i < Connect4.m; i++) {
			for (int j = 0; j < Connect4.n; j++) {
				h += g.focus(c4, i, j);
			}
		}
		
		return h;
	}
}
