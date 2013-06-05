%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Predis

Name:           php-nrk-Predis
Version:        0.8.3
Release:        1%{?dist}
Summary:        Flexible and feature-complete PHP client library for Redis

Group:          Development/Libraries
License:        MIT
URL:            http://pear.nrk.io/package/Predis
Source0:        http://pear.nrk.io/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR)

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(PEAR)
Provides:       php-pear(pear.nrk.io/Predis) = %{version}
BuildRequires:  php-channel(pear.nrk.io)
Requires:       php-channel(pear.nrk.io)

%description
Flexible and feature-complete PHP client library for Redis

%prep
%setup -q -c
[ -f package2.xml ] || mv package.xml package2.xml
mv package2.xml %{pear_name}-%{version}/%{name}.xml

cd %{pear_name}-%{version}


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
rm -rf $RPM_BUILD_ROOT
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_metadir}/.??*

# Install XML package description
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}


%clean
rm -rf $RPM_BUILD_ROOT


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        pear.nrk.io/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}


%{pear_xmldir}/%{name}.xml
# Expand this as needed to avoid owning dirs owned by our dependencies
# and to avoid unowned dirs
%{pear_phpdir}/Predis/Client.php
%{pear_phpdir}/Predis/CommunicationException.php
%{pear_phpdir}/Predis/PredisException.php
%{pear_phpdir}/Predis/Pipeline/MultiExecExecutor.php
%{pear_phpdir}/Predis/Pipeline/SafeClusterExecutor.php
%{pear_phpdir}/Predis/Pipeline/SafeExecutor.php
%{pear_phpdir}/Predis/Pipeline/FireAndForgetExecutor.php
%{pear_phpdir}/Predis/Pipeline/PipelineContext.php
%{pear_phpdir}/Predis/Pipeline/PipelineExecutorInterface.php
%{pear_phpdir}/Predis/Pipeline/StandardExecutor.php
%{pear_phpdir}/Predis/Profile/ServerVersionNext.php
%{pear_phpdir}/Predis/Profile/ServerVersion22.php
%{pear_phpdir}/Predis/Profile/ServerVersion12.php
%{pear_phpdir}/Predis/Profile/ServerProfileInterface.php
%{pear_phpdir}/Predis/Profile/ServerProfile.php
%{pear_phpdir}/Predis/Profile/ServerVersion24.php
%{pear_phpdir}/Predis/Profile/ServerVersion20.php
%{pear_phpdir}/Predis/Profile/ServerVersion26.php
%{pear_phpdir}/Predis/ResponseErrorInterface.php
%{pear_phpdir}/Predis/Monitor/MonitorContext.php
%{pear_phpdir}/Predis/ClientException.php
%{pear_phpdir}/Predis/Replication/ReplicationStrategy.php
%{pear_phpdir}/Predis/NotSupportedException.php
%{pear_phpdir}/Predis/Helpers.php
%{pear_phpdir}/Predis/Transaction/MultiExecContext.php
%{pear_phpdir}/Predis/Transaction/AbortedMultiExecException.php
%{pear_phpdir}/Predis/ResponseObjectInterface.php
%{pear_phpdir}/Predis/Connection/ComposableStreamConnection.php
%{pear_phpdir}/Predis/Connection/ConnectionException.php
%{pear_phpdir}/Predis/Connection/PredisCluster.php
%{pear_phpdir}/Predis/Connection/PhpiredisConnection.php
%{pear_phpdir}/Predis/Connection/ComposableConnectionInterface.php
%{pear_phpdir}/Predis/Connection/WebdisConnection.php
%{pear_phpdir}/Predis/Connection/ConnectionFactory.php
%{pear_phpdir}/Predis/Connection/AbstractConnection.php
%{pear_phpdir}/Predis/Connection/StreamConnection.php
%{pear_phpdir}/Predis/Connection/ReplicationConnectionInterface.php
%{pear_phpdir}/Predis/Connection/ClusterConnectionInterface.php
%{pear_phpdir}/Predis/Connection/PhpiredisStreamConnection.php
%{pear_phpdir}/Predis/Connection/AggregatedConnectionInterface.php
%{pear_phpdir}/Predis/Connection/ConnectionFactoryInterface.php
%{pear_phpdir}/Predis/Connection/MasterSlaveReplication.php
%{pear_phpdir}/Predis/Connection/ConnectionInterface.php
%{pear_phpdir}/Predis/Connection/SingleConnectionInterface.php
%{pear_phpdir}/Predis/Connection/RedisCluster.php
%{pear_phpdir}/Predis/Connection/ConnectionParametersInterface.php
%{pear_phpdir}/Predis/Connection/ConnectionParameters.php
%{pear_phpdir}/Predis/Session/SessionHandler.php
%{pear_phpdir}/Predis/PubSub/AbstractPubSubContext.php
%{pear_phpdir}/Predis/PubSub/DispatcherLoop.php
%{pear_phpdir}/Predis/PubSub/PubSubContext.php
%{pear_phpdir}/Predis/Option/AbstractOption.php
%{pear_phpdir}/Predis/Option/CustomOption.php
%{pear_phpdir}/Predis/Option/ClientExceptions.php
%{pear_phpdir}/Predis/Option/ClientReplication.php
%{pear_phpdir}/Predis/Option/ClientCluster.php
%{pear_phpdir}/Predis/Option/ClientOptions.php
%{pear_phpdir}/Predis/Option/ClientConnectionFactory.php
%{pear_phpdir}/Predis/Option/ClientOptionsInterface.php
%{pear_phpdir}/Predis/Option/ClientPrefix.php
%{pear_phpdir}/Predis/Option/ClientProfile.php
%{pear_phpdir}/Predis/Option/OptionInterface.php
%{pear_phpdir}/Predis/Protocol/ResponseHandlerInterface.php
%{pear_phpdir}/Predis/Protocol/ProtocolException.php
%{pear_phpdir}/Predis/Protocol/ComposableProtocolInterface.php
%{pear_phpdir}/Predis/Protocol/ResponseReaderInterface.php
%{pear_phpdir}/Predis/Protocol/CommandSerializerInterface.php
%{pear_phpdir}/Predis/Protocol/ProtocolInterface.php
%{pear_phpdir}/Predis/Protocol/Text/ComposableTextProtocol.php
%{pear_phpdir}/Predis/Protocol/Text/TextProtocol.php
%{pear_phpdir}/Predis/Protocol/Text/ResponseErrorHandler.php
%{pear_phpdir}/Predis/Protocol/Text/ResponseMultiBulkStreamHandler.php
%{pear_phpdir}/Predis/Protocol/Text/TextResponseReader.php
%{pear_phpdir}/Predis/Protocol/Text/ResponseIntegerHandler.php
%{pear_phpdir}/Predis/Protocol/Text/ResponseBulkHandler.php
%{pear_phpdir}/Predis/Protocol/Text/ResponseStatusHandler.php
%{pear_phpdir}/Predis/Protocol/Text/ResponseMultiBulkHandler.php
%{pear_phpdir}/Predis/Protocol/Text/TextCommandSerializer.php
%{pear_phpdir}/Predis/ExecutableContextInterface.php
%{pear_phpdir}/Predis/Autoloader.php
%{pear_phpdir}/Predis/ResponseQueued.php
%{pear_phpdir}/Predis/Iterator/MultiBulkResponseSimple.php
%{pear_phpdir}/Predis/Iterator/MultiBulkResponse.php
%{pear_phpdir}/Predis/Iterator/MultiBulkResponseTuple.php
%{pear_phpdir}/Predis/Command/ServerFlushAll.php
%{pear_phpdir}/Predis/Command/ListRemove.php
%{pear_phpdir}/Predis/Command/StringSetMultiplePreserve.php
%{pear_phpdir}/Predis/Command/StringSet.php
%{pear_phpdir}/Predis/Command/KeyPreciseExpire.php
%{pear_phpdir}/Predis/Command/HashGetMultiple.php
%{pear_phpdir}/Predis/Command/PubSubUnsubscribe.php
%{pear_phpdir}/Predis/Command/KeyPersist.php
%{pear_phpdir}/Predis/Command/SetAdd.php
%{pear_phpdir}/Predis/Command/PubSubPublish.php
%{pear_phpdir}/Predis/Command/ZSetReverseRange.php
%{pear_phpdir}/Predis/Command/SetDifference.php
%{pear_phpdir}/Predis/Command/PubSubSubscribeByPattern.php
%{pear_phpdir}/Predis/Command/HashIncrementByFloat.php
%{pear_phpdir}/Predis/Command/PrefixHelpers.php
%{pear_phpdir}/Predis/Command/KeyPreciseExpireAt.php
%{pear_phpdir}/Predis/Command/ZSetCardinality.php
%{pear_phpdir}/Predis/Command/PubSubUnsubscribeByPattern.php
%{pear_phpdir}/Predis/Command/SetMove.php
%{pear_phpdir}/Predis/Command/SetRemove.php
%{pear_phpdir}/Predis/Command/ZSetAdd.php
%{pear_phpdir}/Predis/Command/StringGetRange.php
%{pear_phpdir}/Predis/Command/ServerBackgroundSave.php
%{pear_phpdir}/Predis/Command/StringGet.php
%{pear_phpdir}/Predis/Command/ListPopLastPushHead.php
%{pear_phpdir}/Predis/Command/ConnectionEcho.php
%{pear_phpdir}/Predis/Command/StringSubstr.php
%{pear_phpdir}/Predis/Command/ZSetScore.php
%{pear_phpdir}/Predis/Command/KeyRenamePreserve.php
%{pear_phpdir}/Predis/Command/StringAppend.php
%{pear_phpdir}/Predis/Command/ListIndex.php
%{pear_phpdir}/Predis/Command/ServerEvalSHA.php
%{pear_phpdir}/Predis/Command/StringSetBit.php
%{pear_phpdir}/Predis/Command/ZSetRange.php
%{pear_phpdir}/Predis/Command/StringStrlen.php
%{pear_phpdir}/Predis/Command/ServerLastSave.php
%{pear_phpdir}/Predis/Command/ListPopFirst.php
%{pear_phpdir}/Predis/Command/ZSetRank.php
%{pear_phpdir}/Predis/Command/ServerInfoV26x.php
%{pear_phpdir}/Predis/Command/ZSetIntersectionStore.php
%{pear_phpdir}/Predis/Command/SetCardinality.php
%{pear_phpdir}/Predis/Command/StringBitCount.php
%{pear_phpdir}/Predis/Command/TransactionMulti.php
%{pear_phpdir}/Predis/Command/ListPushTail.php
%{pear_phpdir}/Predis/Command/ServerInfo.php
%{pear_phpdir}/Predis/Command/StringGetSet.php
%{pear_phpdir}/Predis/Command/PrefixableCommand.php
%{pear_phpdir}/Predis/Command/HashIncrementBy.php
%{pear_phpdir}/Predis/Command/ServerTime.php
%{pear_phpdir}/Predis/Command/KeyKeys.php
%{pear_phpdir}/Predis/Command/TransactionUnwatch.php
%{pear_phpdir}/Predis/Command/ConnectionAuth.php
%{pear_phpdir}/Predis/Command/HashGet.php
%{pear_phpdir}/Predis/Command/StringIncrement.php
%{pear_phpdir}/Predis/Command/TransactionDiscard.php
%{pear_phpdir}/Predis/Command/SetMembers.php
%{pear_phpdir}/Predis/Command/ServerFlushDatabase.php
%{pear_phpdir}/Predis/Command/HashKeys.php
%{pear_phpdir}/Predis/Command/PubSubSubscribe.php
%{pear_phpdir}/Predis/Command/ConnectionPing.php
%{pear_phpdir}/Predis/Command/ListPopLastBlocking.php
%{pear_phpdir}/Predis/Command/ZSetUnionStore.php
%{pear_phpdir}/Predis/Command/ZSetRemoveRangeByScore.php
%{pear_phpdir}/Predis/Command/ServerEval.php
%{pear_phpdir}/Predis/Command/KeyType.php
%{pear_phpdir}/Predis/Command/ConnectionQuit.php
%{pear_phpdir}/Predis/Command/ListInsert.php
%{pear_phpdir}/Predis/Command/ServerSlaveOf.php
%{pear_phpdir}/Predis/Command/HashValues.php
%{pear_phpdir}/Predis/Command/HashDelete.php
%{pear_phpdir}/Predis/Command/StringPreciseSetExpire.php
%{pear_phpdir}/Predis/Command/ConnectionSelect.php
%{pear_phpdir}/Predis/Command/ZSetIncrementBy.php
%{pear_phpdir}/Predis/Command/TransactionWatch.php
%{pear_phpdir}/Predis/Command/KeyRandom.php
%{pear_phpdir}/Predis/Command/KeyTimeToLive.php
%{pear_phpdir}/Predis/Command/StringIncrementBy.php
%{pear_phpdir}/Predis/Command/ServerConfig.php
%{pear_phpdir}/Predis/Command/ListPopLast.php
%{pear_phpdir}/Predis/Command/ServerMonitor.php
%{pear_phpdir}/Predis/Command/StringSetRange.php
%{pear_phpdir}/Predis/Command/SetUnionStore.php
%{pear_phpdir}/Predis/Command/ServerObject.php
%{pear_phpdir}/Predis/Command/KeyKeysV12x.php
%{pear_phpdir}/Predis/Command/StringDecrementBy.php
%{pear_phpdir}/Predis/Command/HashGetAll.php
%{pear_phpdir}/Predis/Command/ListSet.php
%{pear_phpdir}/Predis/Command/StringIncrementByFloat.php
%{pear_phpdir}/Predis/Command/ServerScript.php
%{pear_phpdir}/Predis/Command/SetRandomMember.php
%{pear_phpdir}/Predis/Command/ListPopLastPushHeadBlocking.php
%{pear_phpdir}/Predis/Command/ZSetRemove.php
%{pear_phpdir}/Predis/Command/HashExists.php
%{pear_phpdir}/Predis/Command/ListPopFirstBlocking.php
%{pear_phpdir}/Predis/Command/StringSetMultiple.php
%{pear_phpdir}/Predis/Command/StringGetBit.php
%{pear_phpdir}/Predis/Command/StringGetMultiple.php
%{pear_phpdir}/Predis/Command/StringBitOp.php
%{pear_phpdir}/Predis/Command/KeyExpire.php
%{pear_phpdir}/Predis/Command/ListTrim.php
%{pear_phpdir}/Predis/Command/StringSetExpire.php
%{pear_phpdir}/Predis/Command/ZSetRangeByScore.php
%{pear_phpdir}/Predis/Command/SetUnion.php
%{pear_phpdir}/Predis/Command/KeyMove.php
%{pear_phpdir}/Predis/Command/ZSetReverseRank.php
%{pear_phpdir}/Predis/Command/ServerSlowlog.php
%{pear_phpdir}/Predis/Command/KeySort.php
%{pear_phpdir}/Predis/Command/KeyExpireAt.php
%{pear_phpdir}/Predis/Command/PrefixableCommandInterface.php
%{pear_phpdir}/Predis/Command/ListPushHead.php
%{pear_phpdir}/Predis/Command/ZSetRemoveRangeByRank.php
%{pear_phpdir}/Predis/Command/AbstractCommand.php
%{pear_phpdir}/Predis/Command/HashSet.php
%{pear_phpdir}/Predis/Command/ServerClient.php
%{pear_phpdir}/Predis/Command/ListLength.php
%{pear_phpdir}/Predis/Command/SetIsMember.php
%{pear_phpdir}/Predis/Command/KeyExists.php
%{pear_phpdir}/Predis/Command/ListPushTailX.php
%{pear_phpdir}/Predis/Command/HashSetPreserve.php
%{pear_phpdir}/Predis/Command/HashLength.php
%{pear_phpdir}/Predis/Command/ServerDatabaseSize.php
%{pear_phpdir}/Predis/Command/KeyPreciseTimeToLive.php
%{pear_phpdir}/Predis/Command/ListPushHeadX.php
%{pear_phpdir}/Predis/Command/SetIntersectionStore.php
%{pear_phpdir}/Predis/Command/SetDifferenceStore.php
%{pear_phpdir}/Predis/Command/ScriptedCommand.php
%{pear_phpdir}/Predis/Command/SetIntersection.php
%{pear_phpdir}/Predis/Command/TransactionExec.php
%{pear_phpdir}/Predis/Command/CommandInterface.php
%{pear_phpdir}/Predis/Command/ServerShutdown.php
%{pear_phpdir}/Predis/Command/KeyDelete.php
%{pear_phpdir}/Predis/Command/StringSetPreserve.php
%{pear_phpdir}/Predis/Command/ZSetCount.php
%{pear_phpdir}/Predis/Command/ListRange.php
%{pear_phpdir}/Predis/Command/HashSetMultiple.php
%{pear_phpdir}/Predis/Command/SetPop.php
%{pear_phpdir}/Predis/Command/Processor/KeyPrefixProcessor.php
%{pear_phpdir}/Predis/Command/Processor/CommandProcessorChainInterface.php
%{pear_phpdir}/Predis/Command/Processor/CommandProcessorInterface.php
%{pear_phpdir}/Predis/Command/Processor/ProcessorChain.php
%{pear_phpdir}/Predis/Command/Processor/CommandProcessingInterface.php
%{pear_phpdir}/Predis/Command/ZSetReverseRangeByScore.php
%{pear_phpdir}/Predis/Command/KeyRename.php
%{pear_phpdir}/Predis/Command/ServerBackgroundRewriteAOF.php
%{pear_phpdir}/Predis/Command/StringDecrement.php
%{pear_phpdir}/Predis/Command/ServerSave.php
%{pear_phpdir}/Predis/ClientInterface.php
%{pear_phpdir}/Predis/Cluster/Distribution/EmptyRingException.php
%{pear_phpdir}/Predis/Cluster/Distribution/DistributionStrategyInterface.php
%{pear_phpdir}/Predis/Cluster/Distribution/HashRing.php
%{pear_phpdir}/Predis/Cluster/Distribution/KetamaPureRing.php
%{pear_phpdir}/Predis/Cluster/CommandHashStrategyInterface.php
%{pear_phpdir}/Predis/Cluster/RedisClusterHashStrategy.php
%{pear_phpdir}/Predis/Cluster/Hash/CRC16HashGenerator.php
%{pear_phpdir}/Predis/Cluster/Hash/HashGeneratorInterface.php
%{pear_phpdir}/Predis/Cluster/PredisClusterHashStrategy.php
%{pear_phpdir}/Predis/ServerException.php
%{pear_phpdir}/Predis/BasicClientInterface.php
%{pear_phpdir}/Predis/ResponseError.php

%{pear_testdir}/Predis


%changelog
