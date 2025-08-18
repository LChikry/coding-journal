class OtherStuff:
    """
    Comprehensive analytics and performance tracking system.
    
    This class demonstrates sophisticated data analysis capabilities:
    - Real-time performance monitoring
    - Statistical analysis of AI behavior
    - Comparative algorithm performance
    - User experience analytics
    
    Features:
    - Move-by-move analytics
    - Cumulative performance tracking
    - Algorithm efficiency comparison
    - Detailed reporting system
    """
    def __init__(self):
        self.analytics = {
            "human": {"nodes_expanded": 0.0, "pruning": 0.0, "moves": 0.0, "avg_time": 0.0},
            "bot": {"nodes_expanded": 0.0, "pruning": 0.0, "ordering_gain": 0.0, "moves": 0.0, "avg_time": 0.0}
        }
        self.move_times = {"human": [], "bot": []}

    def LogMove(self, player, nodes, pruning, ordering_gain=0, move_time=0):
        """
        Advanced move logging with comprehensive statistics.
        
        Tracks:
        - Performance metrics (nodes, pruning, ordering)
        - Timing information
        - Move efficiency analysis
        - Algorithm effectiveness
        """
        self.analytics[player]["nodes_expanded"] += nodes
        self.analytics[player]["pruning"] += pruning
        if player == "bot":
            self.analytics[player]["ordering_gain"] += ordering_gain
        self.analytics[player]["moves"] += 1
        
        # Track timing for performance analysis
        if move_time > 0:
            self.move_times[player].append(move_time)
            self.analytics[player]["avg_time"] = sum(self.move_times[player]) / len(self.move_times[player])

    def DisplayMoveAnalytics(self, player, nodes, pruning, ordering_gain=0):
        """
        Real-time analytics display for move-by-move analysis.
        
        Provides immediate feedback on:
        - Search efficiency
        - Algorithm performance
        - Optimization effectiveness
        - Decision quality
        """
        print(f"\n--- {player.capitalize()} Move Analytics ---")
        print(f"Nodes expanded: {nodes:,}")
        print(f"Pruning performed: {pruning:,}")
        if player == "bot":
            print(f"Ordering gains: {ordering_gain:,}")
            if pruning > 0:
                pruning_efficiency = (pruning / (nodes + pruning)) * 100
                print(f"Pruning efficiency: {pruning_efficiency:.1f}%")
        print("-" * 30)

    def GenerateReport(self):
        """
        Comprehensive final analytics report.
        
        This demonstrates advanced data analysis capabilities:
        - Statistical summaries
        - Performance comparisons
        - Efficiency metrics
        - Algorithm effectiveness analysis
        """
        report_str = "\n" + "="*60
        report_str += "\n           COMPREHENSIVE GAME ANALYTICS REPORT"
        report_str += "\n" + "="*60
        
        for player in self.analytics:
            report_str += f"\n{player.capitalize()} Player Performance:"
            report_str += f"\n  Total moves: {self.analytics[player]['moves']}"
            report_str += f"\n  Total nodes expanded: {self.analytics[player]['nodes_expanded']:,}"
            report_str += f"\n  Total pruning performed: {self.analytics[player]['pruning']:,}"
            
            if player == "bot":
                report_str += f"\n  Total ordering gains: {self.analytics[player]['ordering_gain']:,}"
                if self.analytics[player]['nodes_expanded'] > 0:
                    total_efficiency = (self.analytics[player]['pruning'] / 
                                      (self.analytics[player]['nodes_expanded'] + self.analytics[player]['pruning'])) * 100
                    report_str += f"\n  Overall pruning efficiency: {total_efficiency:.1f}%"
            
            if self.analytics[player]['moves'] > 0:
                avg_nodes = self.analytics[player]['nodes_expanded'] / self.analytics[player]['moves']
                report_str += f"\n  Average nodes per move: {avg_nodes:,.0f}"
            
            if self.analytics[player]['avg_time'] > 0:
                report_str += f"\n  Average move time: {self.analytics[player]['avg_time']:.3f}s"
            
            report_str += "\n"
        
        # Algorithm comparison analysis
        if self.analytics["bot"]["moves"] > 0:
            report_str += "\nAlgorithm Performance Analysis:"
            report_str += f"\n  Search efficiency: {self.analytics['bot']['nodes_expanded']:,} total nodes"
            report_str += f"\n  Optimization effectiveness: {self.analytics['bot']['pruning']:,} branches pruned"
            if self.analytics['bot']['ordering_gain'] > 0:
                report_str += f"\n  Move ordering benefits: {self.analytics['bot']['ordering_gain']:,} additional prunes"
        
        report_str += "\n" + "="*60
        print(report_str)
        return report_str

