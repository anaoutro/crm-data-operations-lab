public class AsterPipelinePageController {
    private AsterPipelineController.PipelineSummary memo;
    public AsterPipelineController.PipelineSummary getSummary() {
        if (memo == null) memo = AsterPipelineController.getPipeline();
        return memo;
    }
}
