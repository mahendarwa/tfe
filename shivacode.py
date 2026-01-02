Hi Andrew,

Thanks for checking on this.

I don’t see body.attachments available as a selectable option in Select an output from previous steps (similar to how attachments appears in Dynamic content).

I tried adding the following expressions manually under the Expression tab, but they don’t seem to work in my case:

triggerOutputs()?['body']?['attachments']

triggerBody()?['attachments']

Could you please confirm the exact expression/path that should be used to reference body.attachments for a Teams webhook trigger? If possible, sharing a sample trigger output structure or the precise expression would help.
