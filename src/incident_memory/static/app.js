const byId = (id) => document.getElementById(id);
const picker = byId('scenario-select');
const runButton = byId('run-button');
const slider = byId('compare-slider');
let scenarioItems = [];
let activeReport = null;

async function init() {
  try {
    const [health, scenarios] = await Promise.all([fetch('/health').then(r => r.json()), fetch('/api/scenarios').then(r => r.json())]);
    byId('opencv-version').textContent = health.opencv_version;
    if(health.aws_s3_artifacts_enabled)byId('deployment-mode').textContent='AWS DEMO';
    if (!health.opencv5) throw new Error(`OpenCV 5 required; service reports ${health.opencv_version}`);
    if (!health.user_uploads_enabled) byId('upload-details').hidden = true;
    scenarioItems = scenarios.items;
    picker.innerHTML = scenarioItems.map(item => `<option value="${escapeHtml(item.id)}">${escapeHtml(label(item.id))}</option>`).join('');
    updateDescription();
  } catch (e) {
    showError(`The service could not initialize: ${e.message}`);
  }
}
function label(id) { return ({dry_normal:'Dry / normal scene',clear_change:'New visible change + water sensor',poor_image:'Blurred / insufficient evidence',lighting_shift:'Lighting shift only',historical_match:'Older history match',camera_movement:'Camera movement',occlusion_blur:'Occlusion + blur'})[id] || id; }
function escapeHtml(value) { return String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
function updateDescription() { const item = scenarioItems.find(x => x.id === picker.value); byId('scenario-copy').textContent = item ? item.description : ''; }
function showError(message) { const box=byId('error'); box.textContent=message; box.hidden=false; }
function setComparison(value) { const pct=Number(value); byId('after-img').style.clipPath=`inset(0 ${100-pct}% 0 0)`; byId('compare-line').style.left=`${pct}%`; }
function classes(arr) { return (arr||[]).map(c=>`<span class="class-chip ${c.toLowerCase()}">${escapeHtml(c)}</span>`).join(''); }
function outcomeText(report) {
  const map={
    possible_visible_water_change:['Possible visible water change — review required','A localized visual difference coincides with an active water-contact event. Appearance supports a hypothesis only; physical presence and cause remain unverified.','HUMAN REVIEW','review'],
    insufficient_evidence:['Insufficient visual evidence','The alarm frame did not meet the image-quality threshold. A retake or second camera view is needed before visual interpretation.','RETAKE REQUESTED','alert'],
    no_credible_visual_water_evidence:['No credible visual evidence of a new water-like change','The illumination-normalized comparison did not produce a qualifying localized candidate. No cause is inferred.','NO VISUAL CHANGE','clear'],
    visually_similar_change_previously_observed:['Similar appearance found in older history','An older pre-event image contains a visually similar region. This weakens the claim that the alarm-time mark is new.','PRE-EXISTING APPEARANCE','clear'],
    observed_change_cause_unverified:['A visual change was observed; cause unverified','The image comparison found a localized change without sufficient independent support for a leak hypothesis.','MORE EVIDENCE','review'],
    sensor_alert_without_credible_visual_change:['Sensor event without visual support','The sensor event is time-aligned, but this comparison did not find a credible localized visual candidate.','MORE EVIDENCE','review'],
    no_incident:['No new change supported','No qualifying visual region was found.','NO NEW CHANGE','clear']
  };
  return map[report.finding]||[report.finding||'Investigation stopped',report.outcome||'Review evidence and trace.','UNVERIFIED','alert'];
}
function renderTrace(trace) {
  byId('trace-count').textContent=`${trace.length} tool calls`;
  byId('trace-list').innerHTML=trace.map((step,i)=>{
    const action=escapeHtml(step.selected_action);
    const result=step.result||{};
    let text='';
    if(action==='evaluate_image_quality') text=`Quality ${result.quality_score}; blur variance ${result.blur_variance}; ${result.usable?'usable':'unusable'}${(result.reasons||[]).length?`: ${result.reasons.join(', ')}`:''}`;
    else if(action==='select_historical_baseline') text=result.selected_frame_id?`Selected ${result.selected_frame_id} at ${result.selected_timestamp}`:'No qualifying baseline';
    else if(action==='align_and_compare') text=`${result.registration_method}; reliability ${result.reliability_score}; ${result.candidate_regions?.length||0} candidate region(s); normalized change ${(100*(result.changed_fraction||0)).toFixed(2)}%`;
    else if(action==='inspect_region') text=`${result.region_id}: ${result.visual_cue}; cause remains unverified`;
    else if(action==='compare_historical_region') text=`Historical region similarity ${result.similarity}; ${result.interpretation}`;
    else if(action==='correlate_sensor_event') text=`${result.sensor_type}: ${result.classification}; time aligned ${result.time_aligned}`;
    else if(action==='retrieve_additional_frame') text=result.available?`Retrieved ${result.frame_id} · ${step.observation_inputs?.reason}`:`No additional frame · ${step.observation_inputs?.reason}`;
    else if(action==='generate_review_request') text=`${result.type}: ${result.reason}`;
    else if(action==='create_evidence_report') text=`Report ${result.report_schema}; ${result.sha256_count} hashed evidence artifact(s)`;
    else text=JSON.stringify(result);
    const refs=(step.evidence_references||[]).length?`<code>Evidence: ${escapeHtml(step.evidence_references.join(' · '))}</code>`:'';
    const err=step.error?`<p class="trace-error">${escapeHtml(step.error)}</p>`:'';
    return `<li class="trace-item"><span class="trace-number">${String(i+1).padStart(2,'0')}</span><span class="trace-action">${action}</span><div class="trace-detail"><p>${escapeHtml(text)}</p>${refs}${err}</div></li>`;
  }).join('');
}
function renderTimeline(report) {
  const steps=[['Historical frame','15 min before alert'],['Alarm event','Sensor event received']];
  if(report.trace?.some(t=>t.selected_action==='retrieve_additional_frame'&&t.result?.available)) steps.splice(1,0,['Older visual record','7 days earlier']);
  byId('history-count').textContent=`${steps.length} references`;
  byId('timeline').innerHTML=steps.map((s,i)=>`<div class="time-step ${i===steps.length-1?'current':''}"><div class="time-dot"></div><strong>${s[0]}</strong><small>${s[1]} · synthetic</small></div>`).join('');
}
function render(report) {
  activeReport = report;
  const [title,summary,badge,badgeClass]=outcomeText(report);
  byId('empty-state').hidden=true; byId('result-view').hidden=false; byId('loading').hidden=true; byId('error').hidden=true;
  byId('outcome-title').textContent=title; byId('outcome-summary').textContent=summary;
  byId('outcome-badge').textContent=badge; byId('outcome-badge').className=`status-badge ${badgeClass}`;
  byId('run-kicker').textContent=`${label(report.scenario)} · ${report.camera_id}`;
  const request=report.review_request; const callout=byId('review-callout');
  if(request){callout.hidden=false; callout.innerHTML=`<strong>${request.type==='operator_review'?'Operator review required':request.type==='retake'?'Request another image':'Review requested'}</strong><p>${escapeHtml(request.reason)}</p><div class="review-actions"><button data-review="approve">Acknowledge</button><button data-review="reject">Reject finding</button><button data-review="request_more_evidence">Request more evidence</button></div><small>These controls record a review decision only; they never control equipment or alarms.</small>`;}else callout.hidden=true;
  byId('before-img').src=report.baseline_data; byId('after-img').src=report.overlay_data||report.event_data; setComparison(slider.value);
  byId('comparison-meta').textContent=report.comparison?`${report.comparison.registration_method} · reliability ${report.comparison.reliability_score}`:'Comparison withheld · quality gate';
  renderTimeline(report); renderTrace(report.trace||[]); byId('evidence-classes').innerHTML=classes(report.evidence_classes);
  const hashes=report.sha256||{}; byId('hash-list').innerHTML=Object.entries(hashes).map(([k,v])=>`<div class="hash-row"><span>${escapeHtml(k)}</span><code>${escapeHtml(v)}</code></div>`).join('')||'<span class="muted-tag">No image hashes available</span>';
  byId('report-link').href=report.report_url; byId('html-report-link').href=report.html_report_data||report.html_report_url; byId('evidence-link').href=report.evidence_url;
  byId('report-note').textContent=report.cloud_evidence?`Evidence bundle stored in private S3 bucket ${report.cloud_evidence.bucket}.`:'JSON report and image evidence are saved locally for this demo run.';
}
async function run() {
  if(!picker.value)return;
  runButton.disabled=true; byId('empty-run').disabled=true; byId('error').hidden=true;
  byId('empty-state').hidden=true; byId('result-view').hidden=true; byId('loading').hidden=false;
  try { const res=await fetch(`/api/investigate/${encodeURIComponent(picker.value)}`); if(!res.ok)throw new Error(`Request failed (${res.status})`); render(await res.json()); }
  catch(e){byId('loading').hidden=true; showError(`Investigation could not be completed: ${e.message}. Check service health and retry.`);}
  finally{runButton.disabled=false; byId('empty-run').disabled=false;}
}
async function uploadPair() {
  const base=byId('baseline-file').files[0], event=byId('event-file').files[0];
  if(!base||!event){showError('Choose both a historical baseline and an alarm-time image.');return;}
  byId('run-button').disabled=true;byId('upload-button').disabled=true;byId('error').hidden=true;byId('result-view').hidden=true;byId('empty-state').hidden=true;byId('loading').hidden=false;
  const form=new FormData();form.append('baseline',base);form.append('event',event);form.append('sensor_active',byId('sensor-active').checked?'true':'false');
  try{const res=await fetch('/api/investigate/upload',{method:'POST',body:form});if(!res.ok){let body={};try{body=await res.json()}catch{}throw new Error(body.detail||`Request failed (${res.status})`)}render(await res.json());}
  catch(e){byId('loading').hidden=true;showError(`Image pair was not processed: ${e.message}`)}
  finally{byId('run-button').disabled=false;byId('upload-button').disabled=false;}
}
async function reviewAction(action) {
  if(!activeReport?.run_storage_id)return;
  const buttons=document.querySelectorAll('[data-review]');buttons.forEach(b=>b.disabled=true);
  try{const res=await fetch(`/api/review/${encodeURIComponent(activeReport.run_storage_id)}`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({action,note:''})});if(!res.ok){const body=await res.json().catch(()=>({}));throw new Error(body.detail||`Review failed (${res.status})`)}const result=await res.json();const note=document.createElement('p');note.className='review-recorded';note.textContent=`Recorded: ${result.review.action.replaceAll('_',' ')} · ${new Date(result.review.recorded_at).toLocaleString()}`;byId('review-callout').append(note);}
  catch(e){showError(`Review could not be recorded: ${e.message}`);buttons.forEach(b=>b.disabled=false);}
}
picker.addEventListener('change',updateDescription); runButton.addEventListener('click',run); byId('empty-run').addEventListener('click',run); byId('upload-button').addEventListener('click',uploadPair);slider.addEventListener('input',()=>setComparison(slider.value));document.addEventListener('click',event=>{const button=event.target.closest('[data-review]');if(button)reviewAction(button.dataset.review)}); init();
