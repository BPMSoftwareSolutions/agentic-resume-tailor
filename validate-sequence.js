#!/usr/bin/env node
/**
 * Simple validation script to check if sequence JSON is well-formed
 */

const fs = require('fs');
const path = require('path');

try {
  // Load schema
  const schemaPath = path.join(__dirname, 'schemas', 'musical-sequence.schema.json');
  const schema = JSON.parse(fs.readFileSync(schemaPath, 'utf8'));
  console.log('✓ Schema loaded successfully');

  // Load sequence
  const sequencePath = path.join(__dirname, 'sequences', 'hybrid-resume-generation.sequence.json');
  const sequence = JSON.parse(fs.readFileSync(sequencePath, 'utf8'));
  console.log('✓ Sequence loaded successfully');

  // Basic validation
  console.log('\n=== Sequence Information ===');
  console.log('ID:', sequence.id);
  console.log('Domain:', sequence.domainId);
  console.log('Name:', sequence.name);
  console.log('Status:', sequence.status);
  console.log('Movements:', sequence.movements.length);

  // Count beats
  let totalBeats = 0;
  sequence.movements.forEach((movement, i) => {
    console.log(`  Movement ${i+1}: ${movement.name} (${movement.beats.length} beats)`);
    totalBeats += movement.beats.length;
  });
  console.log('Total beats:', totalBeats);

  // Check required fields
  console.log('\n=== Required Field Validation ===');
  const requiredFields = ['domainId', 'id', 'name', 'movements', 'userStory'];
  const missingFields = requiredFields.filter(f => !(f in sequence));

  if (missingFields.length === 0) {
    console.log('✓ All required top-level fields present');
  } else {
    console.error('✗ Missing required fields:', missingFields);
    process.exit(1);
  }

  // Validate movements
  console.log('\n=== Movement Validation ===');
  const requiredMovementFields = ['name', 'beats', 'userStory'];
  let movementErrors = [];

  sequence.movements.forEach((movement, i) => {
    const missing = requiredMovementFields.filter(f => !(f in movement));
    if (missing.length > 0) {
      movementErrors.push(`Movement ${i+1} (${movement.name || 'unnamed'}) missing: ${missing.join(', ')}`);
    }
  });

  if (movementErrors.length === 0) {
    console.log('✓ All movements have required fields');
  } else {
    console.error('✗ Movement errors:');
    movementErrors.forEach(e => console.error('  -', e));
    process.exit(1);
  }

  // Validate beats
  console.log('\n=== Beat Validation ===');
  const requiredBeatFields = ['event', 'userStory', 'acceptanceCriteria', 'testFile'];
  let beatErrors = [];

  sequence.movements.forEach((movement, mIdx) => {
    movement.beats.forEach((beat, bIdx) => {
      const missing = requiredBeatFields.filter(f => !(f in beat));
      if (missing.length > 0) {
        beatErrors.push(
          `Movement "${movement.name}" -> Beat ${bIdx+1} (${beat.name || 'unnamed'}) missing: ${missing.join(', ')}`
        );
      }
    });
  });

  if (beatErrors.length === 0) {
    console.log('✓ All beats have required fields');
  } else {
    console.error('✗ Beat errors:');
    beatErrors.forEach(e => console.error('  -', e));
    process.exit(1);
  }

  // Validate user stories
  console.log('\n=== User Story Validation ===');
  const userStoryFields = ['persona', 'goal', 'benefit'];
  let userStoryErrors = [];

  // Check sequence-level user story
  const seqStoryMissing = userStoryFields.filter(f => !(f in (sequence.userStory || {})));
  if (seqStoryMissing.length > 0) {
    userStoryErrors.push(`Sequence-level userStory missing: ${seqStoryMissing.join(', ')}`);
  }

  // Check movement user stories
  sequence.movements.forEach((movement, mIdx) => {
    const movStoryMissing = userStoryFields.filter(f => !(f in (movement.userStory || {})));
    if (movStoryMissing.length > 0) {
      userStoryErrors.push(`Movement "${movement.name}" userStory missing: ${movStoryMissing.join(', ')}`);
    }

    // Check beat user stories
    movement.beats.forEach((beat, bIdx) => {
      const beatStoryMissing = userStoryFields.filter(f => !(f in (beat.userStory || {})));
      if (beatStoryMissing.length > 0) {
        userStoryErrors.push(
          `Movement "${movement.name}" -> Beat "${beat.name}" userStory missing: ${beatStoryMissing.join(', ')}`
        );
      }
    });
  });

  if (userStoryErrors.length === 0) {
    console.log('✓ All user stories have required fields (persona, goal, benefit)');
  } else {
    console.error('✗ User story errors:');
    userStoryErrors.forEach(e => console.error('  -', e));
    process.exit(1);
  }

  console.log('\n✓✓✓ All validations passed! ✓✓✓\n');
  process.exit(0);

} catch (error) {
  console.error('\n✗✗✗ Validation failed! ✗✗✗');
  console.error('Error:', error.message);
  process.exit(1);
}
