import logging

from director.tools.videodb_tool import VideoDBTool
from director.agents.base import BaseAgent, AgentResponse, AgentStatus
from director.core.session import Session, MsgStatus, TextContent
from director.llm.openai import OpenAI

logger = logging.getLogger(__name__)


class IndexCollectionAgent(BaseAgent):
    def __init__(self, session: Session, **kwargs):
        self.agent_name = "index_collection"
        self.description = "Index Collection of videos where you ask gurudev anything about death,karma,relationships, aliens and more"
        self.llm = OpenAI()
        self.parameters = self.get_parameters()
        super().__init__(session=session, **kwargs)

    def run(self, query: str, *args, **kwargs) -> AgentResponse:
        """
        Process the sample based on the given sample ID.

        :param str sample_id: The ID of the sample to process.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        :return: The response containing information about the sample processing operation.
        :rtype: AgentResponse
        """
        try:
            videodb_tool = VideoDBTool(collection_id="c-3c2c6a83-2689-4269-ad81-508b74bf3558")
            for video in videodb_tool.collection.get_videos():
                videodb_tool.index_spoken_words(video)
            self.output_message.actions.append("Indexed Videos for collection..")
            self.output_message.push_update()
            self.output_message.publish()
        except Exception as e:
            logger.exception(f"Error in {self.agent_name}")
            text_content = TextContent(
                agent_name=self.agent_name,
                status=MsgStatus.error,
                status_message="Error in getting the answer.",
            )
            self.output_message.content.append(text_content)
            self.output_message.publish()
            error_message = f"Agent failed with error {e}"
            return AgentResponse(status=AgentStatus.ERROR, message=error_message)
        return AgentResponse(
            status=AgentStatus.SUCCESS,
            message=f"Agent {self.name} completed successfully.",
            data={},
        )
