# OGC API Processes - Part 1 versions 1.0 and 2.0 draft

Part 1 version 1.0 (OGC 18-062r2) and the GeoLabs version 2.0 draft fork
(OGC 18-062r3), hosted as independent part1.v1 and part1.v2 definitions.
Namespace isolation is not a claim of full draft conformance.


Adds a flexible, JSON schema version agnostic documentation to the OGC API Processes standard, supporting further profiling by combining with other Building Blocks.


## Building Blocks

### `ogc.api.processes.part1.v1.parameters.datetime` — datetime

**Type:** parameter

### `ogc.api.processes.part1.v1.parameters.jobId` — jobId

**Type:** parameter

### `ogc.api.processes.part1.v1.parameters.limit` — limit

**Type:** parameter

### `ogc.api.processes.part1.v1.parameters.maxDuration` — maxDuration

**Type:** parameter

### `ogc.api.processes.part1.v1.parameters.minDuration` — minDuration

**Type:** parameter

### `ogc.api.processes.part1.v1.parameters.processIdPathParam` — processIdPathParam

**Type:** parameter

### `ogc.api.processes.part1.v1.parameters.processIdQueryParam` — processIdQueryParam

**Type:** parameter

### `ogc.api.processes.part1.v1.schemas.statusCode` — statusCode

**Type:** schema

### `ogc.api.processes.part1.v1.parameters.type` — type

**Type:** parameter

### `ogc.api.processes.part1.v1.schemas.confClasses` — confClasses

**Type:** schema

### `ogc.api.processes.part1.v1.responses.ExecuteSyncRawRef` — ExecuteSyncRawRef

**Type:** response

### `ogc.api.processes.part1.v1.schemas.exception` — exception

**Type:** schema

### `ogc.api.processes.part1.v1.schemas.additionalParameter` — additionalParameter

**Type:** schema

### `ogc.api.processes.part1.v1.schemas.bbox` — bbox

**Type:** schema

### `ogc.api.processes.part1.v1.schemas.binaryInputValue` — binaryInputValue

**Type:** schema

### `ogc.api.processes.part1.v1.schemas.common-core.confClasses` — confClasses

**Type:** schema

This building block corresponds to the schema for an OGC API Features confClasses

### `ogc.api.processes.part1.v1.schemas.common-core.exception` — exception

**Type:** schema

This building block corresponds to the schema for an OGC API Features exception

### `ogc.api.processes.part1.v1.schemas.link` — link

**Type:** schema

### `ogc.api.processes.part1.v1.schemas.metadata` — metadata

**Type:** schema

### `ogc.api.processes.part1.v1.schemas.subscriber` — subscriber

**Type:** schema

### `ogc.api.processes.part1.v1.schemas.format` — format

**Type:** schema

### `ogc.api.processes.part1.v1.schemas.jobControlOptions` — jobControlOptions

**Type:** schema

### `ogc.api.processes.part1.v1.schemas.transmissionMode` — transmissionMode

**Type:** schema

### `ogc.api.processes.part1.v1.schemas.reference` — reference

**Type:** schema

### `ogc.api.processes.part1.v1.schemas.timeStamp` — timeStamp

**Type:** datatype

This property indicates the time and date when the response was generated

### `ogc.api.processes.part1.v2.parameters.unspecified.f-metadata` — f-metadata

**Type:** parameter

### `ogc.api.processes.part1.v2.responses.common-core.rAPI` — rAPI

**Type:** response

### `ogc.api.processes.part1.v2.parameters.jobId` — jobId

**Type:** parameter

### `ogc.api.processes.part1.v2.parameters.processes-core.prefer-header-return` — prefer-header-return

**Type:** parameter

### `ogc.api.processes.part1.v2.parameters.datetime` — datetime

**Type:** parameter

### `ogc.api.processes.part1.v2.parameters.limit` — limit

**Type:** parameter

### `ogc.api.processes.part1.v2.parameters.maxDuration` — maxDuration

**Type:** parameter

### `ogc.api.processes.part1.v2.parameters.minDuration` — minDuration

**Type:** parameter

### `ogc.api.processes.part1.v2.parameters.processIdPathParam` — processIdPathParam

**Type:** parameter

### `ogc.api.processes.part1.v2.parameters.processIdQueryParam` — processIdQueryParam

**Type:** parameter

### `ogc.api.processes.part1.v2.parameters.processes-core.prefer-header-execution` — prefer-header-execution

**Type:** parameter

### `ogc.api.processes.part1.v2.parameters.processes-core.response` — response

**Type:** parameter

### `ogc.api.processes.part1.v2.schemas.statusCode` — statusCode

**Type:** schema

### `ogc.api.processes.part1.v2.parameters.type` — type

**Type:** parameter

### `ogc.api.processes.part1.v2.responses.processes-core.rEmpty` — rEmpty

**Type:** response

### `ogc.api.processes.part1.v2.responses.processes-core.rExecuteCollectionRedirect` — rExecuteCollectionRedirect

**Type:** response

### `ogc.api.processes.part1.v2.schemas.confClasses` — confClasses

**Type:** schema

### `ogc.api.processes.part1.v2.responses.ExecuteSyncRawRef` — ExecuteSyncRawRef

**Type:** response

### `ogc.api.processes.part1.v2.schemas.exception` — exception

**Type:** schema

### `ogc.api.processes.part1.v2.responses.NotSupported` — NotSupported

**Type:** response

### `ogc.api.processes.part1.v2.schemas.additionalParameter` — additionalParameter

**Type:** schema

### `ogc.api.processes.part1.v2.schemas.processes-core.bbox-def-crs` — bbox-def-crs

**Type:** schema

### `ogc.api.processes.part1.v2.schemas.binaryInputValue` — binaryInputValue

**Type:** schema

### `ogc.api.processes.part1.v2.schemas.binaryValue` — binaryValue

**Type:** schema

### `ogc.api.processes.part1.v2.schemas.common-core.confClasses` — confClasses

**Type:** schema

Compatibility identifier for the official Processes master Common Core confClasses schema.

### `ogc.api.processes.part1.v2.schemas.common-core.exception` — exception

**Type:** schema

This building block corresponds to the schema for an OGC API Features exception

### `ogc.api.processes.part1.v2.schemas.common-core.link` — link

**Type:** schema

### `ogc.api.processes.part1.v2.schemas.processes-core.responseCollection` — responseCollection

**Type:** schema

### `ogc.api.processes.part1.v2.schemas.processes-core.executionUnitRequirements` — executionUnitRequirements

**Type:** schema

### `ogc.api.processes.part1.v2.schemas.jobControlOptions` — jobControlOptions

**Type:** schema

### `ogc.api.processes.part1.v2.schemas.processes-core.linkBase` — linkBase

**Type:** schema

### `ogc.api.processes.part1.v2.schemas.processes-core.linkBaseExtended` — linkBaseExtended

**Type:** schema

### `ogc.api.processes.part1.v2.schemas.processes-core.apis` — apis

**Type:** schema

### `ogc.api.processes.part1.v2.schemas.processes-core.safeCurie` — safeCurie

**Type:** schema

### `ogc.api.processes.part1.v2.schemas.subscriber` — subscriber

**Type:** schema

### `ogc.api.processes.part1.v2.schemas.schema` — schema

**Type:** schema

### `ogc.api.processes.part1.v2.schemas.reference` — reference

**Type:** schema

### `ogc.api.processes.part1.v2.schemas.swagger.schema` — schema

**Type:** schema

### `ogc.api.processes.part1.v2.schemas.timeStamp` — timeStamp

**Type:** datatype

This property indicates the time and date when the response was generated

### `ogc.api.processes.part1.v2.schemas.transmissionMode` — transmissionMode

**Type:** schema

### `ogc.api.processes.part1.v1.parameters.status` — status

**Type:** parameter

### `ogc.api.processes.part1.v1.responses.ConformanceDeclaration` — ConformanceDeclaration

**Type:** response

### `ogc.api.processes.part1.v1.responses.InvalidParameter` — InvalidParameter

**Type:** response

### `ogc.api.processes.part1.v1.responses.NotAllowed` — NotAllowed

**Type:** response

### `ogc.api.processes.part1.v1.responses.NotFound` — NotFound

**Type:** response

### `ogc.api.processes.part1.v1.responses.NotSupported` — NotSupported

**Type:** response

### `ogc.api.processes.part1.v1.responses.ServerError` — ServerError

**Type:** response

### `ogc.api.processes.part1.v1.schemas.inputValueNoObject` — inputValueNoObject

**Type:** schema

### `ogc.api.processes.part1.v1.schemas.common-core.landingPage` — landingPage

**Type:** schema

This building block corresponds to the schema for an OGC API Features landingPage

### `ogc.api.processes.part1.v1.schemas.landingPage` — landingPage

**Type:** schema

### `ogc.api.processes.part1.v1.schemas.statusInfo` — statusInfo

**Type:** schema

### `ogc.api.processes.part1.v1.schemas.descriptionType` — descriptionType

**Type:** schema

### `ogc.api.processes.part1.v1.schemas.output` — output

**Type:** schema

### `ogc.api.processes.part1.v1.schemas.schema` — schema

**Type:** schema

### `ogc.api.processes.part1.v1.schemas.swagger.schema` — schema

**Type:** schema

### `ogc.api.processes.part1.v2.parameters.status` — status

**Type:** parameter

### `ogc.api.processes.part1.v2.responses.ConformanceDeclaration` — ConformanceDeclaration

**Type:** response

### `ogc.api.processes.part1.v2.responses.InvalidParameter` — InvalidParameter

**Type:** response

### `ogc.api.processes.part1.v2.responses.NotAllowed` — NotAllowed

**Type:** response

### `ogc.api.processes.part1.v2.responses.NotFound` — NotFound

**Type:** response

### `ogc.api.processes.part1.v2.responses.ServerError` — ServerError

**Type:** response

### `ogc.api.processes.part1.v2.responses.common-core.rNotAcceptable` — rNotAcceptable

**Type:** response

### `ogc.api.processes.part1.v2.schemas.bbox` — bbox

**Type:** schema

### `ogc.api.processes.part1.v2.schemas.common-core.landingPage` — landingPage

**Type:** schema

This building block corresponds to the schema for an OGC API Features landingPage

### `ogc.api.processes.part1.v2.schemas.landingPage` — landingPage

**Type:** schema

### `ogc.api.processes.part1.v2.schemas.processes-core.dataAccessAPIs` — dataAccessAPIs

**Type:** schema

### `ogc.api.processes.part1.v2.schemas.processes-core.processingEntityType` — processingEntityType

**Type:** schema

### `ogc.api.processes.part1.v2.schemas.processes-core.dataClasses` — dataClasses

**Type:** schema

### `ogc.api.processes.part1.v2.schemas.processes-core.schemaAndOccurrences` — schemaAndOccurrences

**Type:** schema

### `ogc.api.processes.part1.v2.schemas.swagger.inputDescription` — inputDescription

**Type:** schema

### `ogc.api.processes.part1.v2.schemas.swagger.outputDescription` — outputDescription

**Type:** schema

### `ogc.api.processes.part1.v1.paths.Conformance` — Conformance

**Type:** path

### `ogc.api.processes.part1.v1.schemas.inputValue` — inputValue

**Type:** schema

### `ogc.api.processes.part1.v1.responses.LandingPage` — LandingPage

**Type:** response

### `ogc.api.processes.part1.v1.responses.ExecuteAsync` — ExecuteAsync

**Type:** response

### `ogc.api.processes.part1.v1.responses.Status` — Status

**Type:** response

### `ogc.api.processes.part1.v1.schemas.jobList` — jobList

**Type:** schema

### `ogc.api.processes.part1.v1.schemas.processSummary` — processSummary

**Type:** schema

### `ogc.api.processes.part1.v1.schemas.inputDescription` — inputDescription

**Type:** schema

### `ogc.api.processes.part1.v1.schemas.outputDescription` — outputDescription

**Type:** schema

### `ogc.api.processes.part1.v1.schemas.swagger.inputDescription` — inputDescription

**Type:** schema

### `ogc.api.processes.part1.v1.schemas.swagger.outputDescription` — outputDescription

**Type:** schema

### `ogc.api.processes.part1.v2.paths.Conformance` — Conformance

**Type:** path

### `ogc.api.processes.part1.v2.responses.LandingPage` — LandingPage

**Type:** response

### `ogc.api.processes.part1.v2.schemas.format` — format

**Type:** schema

### `ogc.api.processes.part1.v2.schemas.link` — link

**Type:** schema

### `ogc.api.processes.part1.v2.schemas.swagger.process` — process

**Type:** schema

### `ogc.api.processes.part1.v1.schemas.qualifiedInputValue` — qualifiedInputValue

**Type:** schema

### `ogc.api.processes.part1.v1.paths.LandingPage` — LandingPage

**Type:** path

### `ogc.api.processes.part1.v1.paths.DismissJob` — Dismiss Job

**Type:** path

### `ogc.api.processes.part1.v1.paths.Job` — Job

**Type:** path

### `ogc.api.processes.part1.v1.responses.JobList` — JobList

**Type:** response

### `ogc.api.processes.part1.v1.schemas.processList` — processList

**Type:** schema

### `ogc.api.processes.part1.v1.schemas.process` — process

**Type:** schema

### `ogc.api.processes.part1.v1.schemas.swagger.process` — process

**Type:** schema

### `ogc.api.processes.part1.v2.paths.LandingPage` — LandingPage

**Type:** path

### `ogc.api.processes.part1.v2.schemas.collectionValue` — collectionValue

**Type:** schema

### `ogc.api.processes.part1.v2.schemas.output` — output

**Type:** schema

### `ogc.api.processes.part1.v2.schemas.metadata` — metadata

**Type:** schema

### `ogc.api.processes.part1.v2.responses.swagger.ProcessDescription` — ProcessDescription

**Type:** response

### `ogc.api.processes.part1.v1.schemas.inlineOrRefData` — inlineOrRefData

**Type:** schema

### `ogc.api.processes.part1.v1.paths.JobList` — JobList

**Type:** path

### `ogc.api.processes.part1.v1.responses.ProcessList` — ProcessList

**Type:** response

### `ogc.api.processes.part1.v1.responses.ProcessDescription` — ProcessDescription

**Type:** response

### `ogc.api.processes.part1.v1.responses.swagger.ProcessDescription` — ProcessDescription

**Type:** response

### `ogc.api.processes.part1.v2.schemas.inputValueNoObject` — inputValueNoObject

**Type:** schema

### `ogc.api.processes.part1.v2.schemas.valueNoObject` — valueNoObject

**Type:** schema

### `ogc.api.processes.part1.v2.schemas.descriptionType` — descriptionType

**Type:** schema

### `ogc.api.processes.part1.v1.schemas.execute` — execute

**Type:** schema

### `ogc.api.processes.part1.v1.schemas.results` — results

**Type:** schema

### `ogc.api.processes.part1.v1.paths.ProcessList` — ProcessList

**Type:** path

### `ogc.api.processes.part1.v1.paths.ProcessDescription` — ProcessDescription

**Type:** path

### `ogc.api.processes.part1.v2.schemas.inputValue` — inputValue

**Type:** schema

### `ogc.api.processes.part1.v2.schemas.value` — value

**Type:** schema

### `ogc.api.processes.part1.v2.schemas.inputDescription` — inputDescription

**Type:** schema

### `ogc.api.processes.part1.v2.schemas.outputDescription` — outputDescription

**Type:** schema

### `ogc.api.processes.part1.v2.schemas.processSummary` — processSummary

**Type:** schema

### `ogc.api.processes.part1.v2.schemas.statusInfo` — statusInfo

**Type:** schema

### `ogc.api.processes.part1.v1.responses.ExecuteSync` — ExecuteSync

**Type:** response

### `ogc.api.processes.part1.v1.responses.Results` — Results

**Type:** response

### `ogc.api.processes.part1.v2.schemas.qualifiedInputValue` — qualifiedInputValue

**Type:** schema

### `ogc.api.processes.part1.v2.schemas.qualifiedValue` — qualifiedValue

**Type:** schema

### `ogc.api.processes.part1.v2.schemas.process` — process

**Type:** schema

### `ogc.api.processes.part1.v2.schemas.processList` — processList

**Type:** schema

### `ogc.api.processes.part1.v2.responses.ExecuteAsync` — ExecuteAsync

**Type:** response

### `ogc.api.processes.part1.v2.responses.Status` — Status

**Type:** response

### `ogc.api.processes.part1.v2.schemas.jobList` — jobList

**Type:** schema

### `ogc.api.processes.part1.v1.paths.Execution` — Execute

**Type:** path

### `ogc.api.processes.part1.v1.paths.JobResult` — Job result

**Type:** path

### `ogc.api.processes.part1.v2.schemas.inlineOrRefData` — inlineOrRefData

**Type:** schema

### `ogc.api.processes.part1.v2.responses.ProcessDescription` — ProcessDescription

**Type:** response

### `ogc.api.processes.part1.v2.responses.ProcessList` — ProcessList

**Type:** response

### `ogc.api.processes.part1.v2.paths.DismissJob` — Dismiss Job

**Type:** path

### `ogc.api.processes.part1.v2.paths.Job` — Job

**Type:** path

### `ogc.api.processes.part1.v2.responses.JobList` — JobList

**Type:** response

### `ogc.api.processes.part1.v1.api` — OGC API - Processes: Part 1

**Type:** api

This building block corresponds to OGC API Processes Part 1

### `ogc.api.processes.part1.v2.schemas.processes-core.values` — values

**Type:** schema

### `ogc.api.processes.part1.v2.paths.ProcessDescription` — ProcessDescription

**Type:** path

### `ogc.api.processes.part1.v2.operations.oProcessList` — oProcessList

**Type:** model

### `ogc.api.processes.part1.v2.paths.JobList` — JobList

**Type:** path

### `ogc.api.processes.part1.v2.schemas.processes-core.executeBase` — executeBase

**Type:** schema

### `ogc.api.processes.part1.v2.schemas.results` — results

**Type:** schema

### `ogc.api.processes.part1.v2.paths.ProcessList` — ProcessList

**Type:** path

### `ogc.api.processes.part1.v2.schemas.execute` — execute

**Type:** schema

### `ogc.api.processes.part1.v2.responses.ExecuteSync` — ExecuteSync

**Type:** response

### `ogc.api.processes.part1.v2.responses.Results` — Results

**Type:** response

### `ogc.api.processes.part1.v2.paths.Execution` — Execute

**Type:** path

### `ogc.api.processes.part1.v2.operations.oJobResults` — oJobResults

**Type:** model

### `ogc.api.processes.part1.v2.paths.JobResult` — Job result

**Type:** path

### `ogc.api.processes.part1.v2.api` — OGC API - Processes: Part 1

**Type:** api

This building block corresponds to OGC API Processes

