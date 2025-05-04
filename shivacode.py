SET ANSI_NULLS ON;
SET QUOTED_IDENTIFIER ON;

CREATE TABLE [dbo].[authservice_audit] (
    [referralid] char(15) NOT NULL,
    [sequence] int NOT NULL,
    [globaltemplate] char(1) NOT NULL,
    [operation] char(15) NOT NULL,
    [op_columns] varbinary(256) NULL,
    [op_date] datetime(2) NOT NULL,
    [op_user] varchar(120) NULL,
    [op_app] varchar(512) NULL,
    [op_host] varchar(512) NULL,
    [codeid] char(15) NULL,
    [catid] char(15) NULL,
    [subcatid] char(15) NULL,
    [svcgroupid] char(15) NULL,
    [totalunits] int NULL,
    [actualunits] int NULL,
    [modcode] char(2) NULL,
    [modcode2] char(2) NULL,
    [modcode3] char(2) NULL,
    [modcode4] char(2) NULL,
    [modcode5] char(2) NULL,
    [negotiatedcontract] char(15) NULL,
    [negotiatedterm] char(15) NULL,
    [negotiatedvalue] money NULL,
    [status] char(10) NULL,
    [DeterminationDate] smalldatetime NULL,
    [IcdVersion] char(1) NULL,
    [PrinDiag] varchar(8) NULL,
    [Diag1] char(2) NULL,
    [Diag2] char(2) NULL,
    [Diag3] char(2) NULL,
    [Diag4] char(2) NULL,
    [Diag5] char(2) NULL,
    [Diag6] char(2) NULL,
    [Diag7] char(2) NULL,
    [Diag8] char(2) NULL,
    [dosdate] smalldatetime NULL,
    [DosTo] smalldatetime NULL,
    [StatusOverride] char(1) NULL,
    [SvcFrequency] varchar(10) NULL
)
ON [PRIMARY]
WITH (DATA_COMPRESSION = NONE);

ALTER TABLE [dbo].[authservice_audit] SET (LOCK_ESCALATION = TABLE);
