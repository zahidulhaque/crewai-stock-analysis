"""
CrewAI Callbacks for Progress Tracking
"""
import logging
from typing import Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class AnalysisCallbacks:
    """Callbacks for tracking analysis progress"""

    def __init__(self, progress_callback=None, status_callback=None):
        """
        Initialize callbacks

        Args:
            progress_callback: Function to call with progress updates (0-100)
            status_callback: Function to call with status messages
        """
        self.progress_callback = progress_callback
        self.status_callback = status_callback
        self.task_count = 0
        self.completed_tasks = 0
        self.start_time = None

    def on_crew_start(self, crew: Any, inputs: dict):
        """Called when crew starts execution"""
        self.start_time = datetime.now()
        logger.info(f"Crew started with inputs: {inputs}")
        if self.status_callback:
            self.status_callback(f"🚀 Starting analysis for {inputs.get('stock_symbol', 'N/A')}...")

    def on_task_start(self, task: Any):
        """Called when a task starts"""
        self.task_count += 1
        task_name = getattr(task, 'description', 'Unknown task')[:60]
        logger.info(f"Task started: {task_name}")
        if self.status_callback:
            self.status_callback(f"⚙️  {task_name}...")

    def on_task_complete(self, task: Any, output: Any):
        """Called when a task completes"""
        self.completed_tasks += 1
        task_name = getattr(task, 'description', 'Unknown task')[:60]
        logger.info(f"Task completed: {task_name}")

        # Calculate progress
        if self.task_count > 0:
            progress = int((self.completed_tasks / max(self.task_count, 1)) * 100)
            if self.progress_callback:
                self.progress_callback(progress)

        if self.status_callback:
            self.status_callback(f"✅ Completed: {task_name}")

    def on_agent_start(self, agent: Any, task: Any):
        """Called when an agent starts working on a task"""
        agent_role = getattr(agent, 'role', 'Unknown agent')
        logger.debug(f"Agent '{agent_role}' started working")

    def on_agent_finish(self, agent: Any, output: Any):
        """Called when an agent finishes"""
        agent_role = getattr(agent, 'role', 'Unknown agent')
        logger.debug(f"Agent '{agent_role}' finished")

    def on_tool_start(self, tool: Any, input_data: str):
        """Called when a tool starts execution"""
        tool_name = getattr(tool, 'name', 'Unknown tool')
        logger.debug(f"Tool '{tool_name}' started with input: {input_data[:100]}")

    def on_tool_end(self, tool: Any, output: str):
        """Called when a tool finishes execution"""
        tool_name = getattr(tool, 'name', 'Unknown tool')
        logger.debug(f"Tool '{tool_name}' completed")

    def on_crew_finish(self, crew: Any, output: Any):
        """Called when crew finishes execution"""
        if self.start_time:
            elapsed = (datetime.now() - self.start_time).total_seconds()
            logger.info(f"Crew finished in {elapsed:.2f} seconds")
            if self.status_callback:
                self.status_callback(f"🎉 Analysis completed in {elapsed:.1f}s")

        if self.progress_callback:
            self.progress_callback(100)


class StreamlitCallbacks(AnalysisCallbacks):
    """Streamlit-specific callbacks"""

    def __init__(self, progress_bar=None, status_text=None):
        """
        Initialize Streamlit callbacks

        Args:
            progress_bar: Streamlit progress bar object
            status_text: Streamlit text object for status updates
        """
        super().__init__()
        self.progress_bar = progress_bar
        self.status_text = status_text

    def on_crew_start(self, crew: Any, inputs: dict):
        """Called when crew starts"""
        super().on_crew_start(crew, inputs)
        if self.progress_bar:
            self.progress_bar.progress(0)
        if self.status_text:
            stock = inputs.get('stock_symbol', 'N/A')
            market = inputs.get('market', 'N/A')
            self.status_text.text(f"🚀 Starting analysis for {stock} ({market} market)")

    def on_task_start(self, task: Any):
        """Called when task starts"""
        super().on_task_start(task)
        if self.status_text:
            task_desc = getattr(task, 'description', 'Processing')[:80]
            self.status_text.text(f"⚙️  {task_desc}...")

    def on_task_complete(self, task: Any, output: Any):
        """Called when task completes"""
        super().on_task_complete(task, output)

        # Update progress bar
        if self.progress_bar and self.task_count > 0:
            progress = self.completed_tasks / max(self.task_count, 1)
            self.progress_bar.progress(progress)

        if self.status_text:
            task_desc = getattr(task, 'description', 'Task')[:60]
            self.status_text.text(f"✅ Completed: {task_desc}")

    def on_crew_finish(self, crew: Any, output: Any):
        """Called when crew finishes"""
        super().on_crew_finish(crew, output)
        if self.progress_bar:
            self.progress_bar.progress(1.0)
        if self.status_text:
            if self.start_time:
                elapsed = (datetime.now() - self.start_time).total_seconds()
                self.status_text.text(f"🎉 Analysis completed successfully in {elapsed:.1f}s!")
            else:
                self.status_text.text("🎉 Analysis completed successfully!")
